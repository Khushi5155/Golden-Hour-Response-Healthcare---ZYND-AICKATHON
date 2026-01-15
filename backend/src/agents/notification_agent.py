from src.services.notification_service import notification_service
from src.zynd.mock_zynd import zynd_registry


class NotificationAgent:
    """Agent responsible for alerting relevant parties."""
    did = "did:zynd:agent_notification_ghi999"
    name = "Notification Agent"

    async def send_emergency_alert(self, emergency_data: dict, hospital_data: dict):
        hospital_subject = (
            f"URGENT: Incoming Emergency - {emergency_data.get('severity', 'UNKNOWN')}"
        )
        hospital_body = f"""
        EMERGENCY ALERT
        --------------------------------
        Severity: {emergency_data.get('severity')}
        Type: {emergency_data.get('description')}
        Patient Location: {emergency_data.get('address', 'GPS Coords Only')}
        
        ETA: {hospital_data['route_info']['duration_min']} minutes
        Distance: {hospital_data['route_info']['distance_km']} km
        """

        await notification_service.send_email(
            recipient_email=emergency_data.get("contact_email"),
            subject=hospital_subject,
            body=hospital_body,
        )

        return {"status": "alerts_sent"}


notification_agent = NotificationAgent()

async def _notification_handler(payload: dict):
    return await notification_agent.send_emergency_alert(
        payload["emergency_data"], payload["hospital_data"]
    )

zynd_registry.register_agent(notification_agent.did, _notification_handler)
