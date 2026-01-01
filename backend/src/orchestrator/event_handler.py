from agents.triage_agent import TriageAgent
from agents.routing_agent import RoutingAgent
from agents.notification_agent import NotificationAgent


class EmergencyOrchestrator:

    def __init__(self):
        self.triage_agent = TriageAgent()
        self.routing_agent = RoutingAgent()
        self.notification_agent = NotificationAgent()

    def handle_emergency(self, emergency_id: int, payload: dict):
        """
        Handle emergency with emergency_id and payload
        """
        print(f"🚨 Orchestrator processing Emergency ID: {emergency_id}")
        
        # Execute triage analysis
        triage_result = self.triage_agent.execute(payload)

        # Route to appropriate hospital
        routing_result = self.routing_agent.execute({
            "severity": triage_result["severity"],
            "location": payload.get("location")
        })

        # Send notifications
        notification_result = self.notification_agent.execute({
            "emergency_id": emergency_id,
            "triage": triage_result,
            "routing": routing_result
        })

        return {
            "emergency_id": emergency_id,
            "triage": triage_result,
            "routing": routing_result,
            "notification": notification_result
        }
