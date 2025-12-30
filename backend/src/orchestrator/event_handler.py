from agents.triage_agent import TriageAgent
from agents.routing_agent import RoutingAgent
from agents.notification_agent import NotificationAgent

class EmergencyOrchestrator:

    def __init__(self):
        self.triage_agent = TriageAgent()
        self.routing_agent = RoutingAgent()
        self.notification_agent = NotificationAgent()

    def handle_emergency(self, payload: dict):
        triage_result = self.triage_agent.execute(payload)

        routing_result = self.routing_agent.execute({
            "severity": triage_result["severity"]
        })

        notification_result = self.notification_agent.execute({
            "triage": triage_result,
            "routing": routing_result
        })

        return {
            "triage": triage_result,
            "routing": routing_result,
            "notification": notification_result
        }
