from src.services.maps_service import maps_service
from src.zynd.mock_zynd import zynd_registry


class RoutingAgent:
    did = "did:zynd:agent_routing_def456"
    name = "Routing Agent"

    async def find_best_hospital(self, emergency_location: tuple, hospitals: list):
        evaluated_hospitals = []

        for hospital in hospitals:
            route_info = await maps_service.get_route_details(
                emergency_location, hospital["coords"]
            )

            if route_info:
                hospital_data = hospital.copy()
                hospital_data["route_info"] = route_info
                evaluated_hospitals.append(hospital_data)

        evaluated_hospitals.sort(key=lambda x: x["route_info"]["duration_min"])

        if not evaluated_hospitals:
            return None

        return evaluated_hospitals[0]

    async def execute(self, payload: dict):
        return await self.find_best_hospital(
            payload["emergency_location"], payload["hospitals"]
        )


routing_agent = RoutingAgent()

async def _routing_handler(payload: dict):
    return await routing_agent.execute(payload)

zynd_registry.register_agent(routing_agent.did, _routing_handler)
