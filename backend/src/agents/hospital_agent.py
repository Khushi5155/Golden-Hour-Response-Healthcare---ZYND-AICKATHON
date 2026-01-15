from src.agents.base_agent import BaseAgent
from src.services.maps_service import maps_service
from src.zynd.mock_zynd import zynd_registry


class HospitalAgent(BaseAgent):
    """Agent to select hospitals based on severity, availability, and distance."""

    def __init__(self):
        super().__init__(
            did="did:zynd:agent_hospital_xyz789",
            name="Hospital Agent"
        )

    async def find_suitable_hospitals(
        self,
        severity: str,
        location: tuple,
        required_specialists: list,
        hospital_db: list,
    ):
        suitable_hospitals = []

        for hospital in hospital_db:
            if severity == "RED" and hospital.get("icu_beds_available", 0) < 1:
                continue
            elif severity == "YELLOW" and hospital.get("emergency_beds_available", 0) < 1:
                continue

            has_specialists = all(
                spec in hospital.get("specialists", [])
                for spec in required_specialists
            )
            if not has_specialists:
                continue

            route_info = await maps_service.get_route_details(
                location, hospital["coords"]
            )
            if not route_info:
                continue

            hospital_copy = hospital.copy()
            hospital_copy.update(
                {
                    "distance_km": route_info["distance_km"],
                    "eta_minutes": route_info["duration_min"],
                    "has_specialists": has_specialists,
                }
            )

            suitable_hospitals.append(hospital_copy)

        suitable_hospitals.sort(
            key=lambda x: (
                x.get("distance_km", 999),
                -(x.get("icu_beds_available", 0)
                  + x.get("emergency_beds_available", 0)),
            )
        )

        return suitable_hospitals[:5]

    async def execute(self, payload: dict) -> list:
        return await self.find_suitable_hospitals(
            severity=payload["severity"],
            location=payload["location"],
            required_specialists=payload["required_specialists"],
            hospital_db=payload["hospital_db"],
        )


hospital_agent = HospitalAgent()

# ❗ Because execute is async, wrap it so registry can await it
async def _hospital_handler(payload: dict):
    return await hospital_agent.execute(payload)

zynd_registry.register_agent(hospital_agent.did, _hospital_handler)
