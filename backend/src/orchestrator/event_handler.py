# src/orchestrator/event_handler.py  (or wherever this lives)

from typing import Dict, Any

from src.agents.triage_agent import triage_agent
from src.agents.routing_agent import routing_agent
from src.agents.notification_agent import notification_agent
from src.zynd.mock_zynd import zynd_registry


class EmergencyOrchestrator:
    """
    Lightweight Zynd-style orchestrator for simple event-based flows.
    Uses DIDs + registry instead of direct .execute() calls.
    """

    def __init__(self):
        self.triage_did = triage_agent.did
        self.routing_did = routing_agent.did
        self.notification_did = notification_agent.did

    async def handle_emergency(self, emergency_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle emergency with emergency_id and payload.
        """
        print(f"🚨 Orchestrator processing Emergency ID: {emergency_id}")

        # 1️⃣ TRIAGE via Zynd
        triage_result = await zynd_registry.call(self.triage_did, payload)

        # 2️⃣ ROUTING via Zynd
        routing_result = await zynd_registry.call(
            self.routing_did,
            {
                "emergency_location": payload.get("location"),
                "hospitals": payload.get("candidate_hospitals", []),
            },
        )

        # 3️⃣ NOTIFICATION via Zynd
        notification_result = await zynd_registry.call(
            self.notification_did,
            {
                "emergency_data": {
                    "severity": triage_result["severity"],
                    "priority": triage_result["priority"],
                    "description": payload.get("description", ""),
                    "address": payload.get("address", ""),
                    "contact_email": payload.get("contact_email"),
                },
                "hospital_data": routing_result,
            },
        )

        return {
            "emergency_id": emergency_id,
            "triage": triage_result,
            "routing": routing_result,
            "notification": notification_result,
        }


orchestrator = EmergencyOrchestrator()
