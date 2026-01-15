from fastapi import HTTPException
import uuid

from src.agents.triage_agent import triage_agent
from src.agents.hospital_agent import hospital_agent
from src.agents.routing_agent import routing_agent
from src.agents.notification_agent import notification_agent
from src.services.maps_service import maps_service
from src.database.db import MOCK_HOSPITALS
from src.zynd.mock_zynd import zynd_registry


class EmergencyOrchestrator:
    """
    Central coordinator that manages the emergency workflow:
    Triage → Hospital → Routing → Notification
    Now routed through a Zynd-style registry.
    """

    def __init__(self):
        self.triage_did = triage_agent.did
        self.hospital_did = hospital_agent.did
        self.routing_did = routing_agent.did
        self.notification_did = notification_agent.did

    async def handle_emergency(self, request, background_tasks):
        request_id = str(uuid.uuid4())

        # 1️⃣ TRIAGE via Zynd
        triage_input = {
            "symptoms": request.symptoms,
            "vitals": request.vitals,
            "age": request.age,
        }
        triage_result = await zynd_registry.call(self.triage_did, triage_input)

        # 2️⃣ Address from maps_service
        address = await maps_service.get_location_address(
            request.location.lat, request.location.lng
        )
        emergency_coords = (request.location.lat, request.location.lng)

        # 3️⃣ HOSPITALS via Zynd
        top_hospitals = await zynd_registry.call(
            self.hospital_did,
            {
                "severity": triage_result["severity"],
                "location": emergency_coords,
                "required_specialists": triage_result["recommended_specialists"],
                "hospital_db": MOCK_HOSPITALS,
            },
        )

        if not top_hospitals:
            raise HTTPException(
                status_code=404, detail="No suitable hospitals found"
            )

        routing_candidates = [
            {"id": h["id"], "name": h["name"], "coords": h["coords"]}
            for h in top_hospitals
        ]

        # 4️⃣ ROUTING via Zynd
        best_hospital = await zynd_registry.call(
            self.routing_did,
            {
                "emergency_location": emergency_coords,
                "hospitals": routing_candidates,
            },
        )

        if not best_hospital:
            raise HTTPException(
                status_code=404, detail="No reachable hospitals found"
            )

        # 5️⃣ NOTIFICATION via Zynd (background)
        emergency_data = {
            "severity": triage_result["severity"],
            "priority": triage_result["priority"],
            "description": request.description,
            "address": address,
            "contact_email": request.contact_email,
        }

        background_tasks.add_task(
            zynd_registry.call,
            self.notification_did,
            {
                "emergency_data": emergency_data,
                "hospital_data": best_hospital,
            },
        )

        # 6️⃣ RESPONSE
        return {
            "request_id": request_id,
            "status": "success",
            "triage_result": triage_result,
            "assigned_hospital": best_hospital["name"],
            "eta_minutes": best_hospital["route_info"]["duration_min"],
            "top_hospitals": top_hospitals,
            "detected_address": address,
        }


orchestrator = EmergencyOrchestrator()
