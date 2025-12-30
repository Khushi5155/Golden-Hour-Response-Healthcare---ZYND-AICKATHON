import os
import sys

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database.db import SessionLocal, Emergency, AgentLog
from datetime import datetime


def create_test_emergency():
    """Create a realistic test emergency with agent logs"""
    db = SessionLocal()
    
    print("🚑 Creating Test Emergency...")
    print()
    
    try:
        # Create emergency
        emergency = Emergency(
            location="Connaught Place, Central Delhi",
            latitude=28.6289,
            longitude=77.2065,
            symptoms=["chest_pain", "shortness_of_breath", "sweating"],
            age_group="60+",
            vitals={"bp": "180/100", "heart_rate": 125},
            severity="RED",
            priority=1,
            status="REGISTERED"
        )
        
        db.add(emergency)
        db.commit()
        db.refresh(emergency)
        
        print(f"✅ Emergency Created (ID: {emergency.id})")
        print(f"   📍 Location: {emergency.location}")
        print(f"   🚨 Severity: {emergency.severity}")
        print(f"   👤 Age Group: {emergency.age_group}")
        print(f"   💊 Symptoms: {', '.join(emergency.symptoms)}")
        print()
        
        # Create agent logs
        logs = [
            AgentLog(
                agent_id="did:zynd:agent:triage:abc123",
                agent_type="triage",
                agent_name="Emergency Triage Agent",
                emergency_id=emergency.id,
                action="Classified severity as RED - Critical cardiac event",
                input_data={
                    "symptoms": emergency.symptoms,
                    "age_group": emergency.age_group,
                    "vitals": emergency.vitals
                },
                output_data={
                    "severity": "RED",
                    "priority": 1,
                    "recommended_specialists": ["cardiologist", "emergency_physician"],
                    "confidence": 0.96
                },
                processing_time_ms=187,
                success="SUCCESS"
            ),
            AgentLog(
                agent_id="did:zynd:agent:hospital:def456",
                agent_type="hospital",
                agent_name="Hospital Assignment Agent",
                emergency_id=emergency.id,
                action="Assigned Max Hospital Saket - 3.2km away, 5 ICU beds available",
                input_data={
                    "severity": "RED",
                    "location": {"lat": 28.6289, "lng": 77.2065},
                    "required_specialists": ["cardiologist"]
                },
                output_data={
                    "hospital_id": "max_hospital_saket",
                    "hospital_name": "Max Hospital, Saket",
                    "distance_km": 3.2,
                    "icu_beds": 5,
                    "eta_minutes": 12
                },
                processing_time_ms=423,
                success="SUCCESS"
            ),
            AgentLog(
                agent_id="did:zynd:agent:routing:ghi789",
                agent_type="routing",
                agent_name="Ambulance Routing Agent",
                emergency_id=emergency.id,
                action="Dispatched AMB-001, ETA 12 minutes",
                input_data={
                    "emergency_location": {"lat": 28.6289, "lng": 77.2065},
                    "hospital_location": {"lat": 28.5245, "lng": 77.2060},
                    "traffic_condition": "moderate"
                },
                output_data={
                    "ambulance_id": "AMB-001",
                    "eta_minutes": 12,
                    "route_distance_km": 3.2,
                    "driver_name": "Rajesh Kumar",
                    "vehicle_type": "Advanced Life Support (ALS)"
                },
                processing_time_ms=567,
                success="SUCCESS"
            ),
            AgentLog(
                agent_id="did:zynd:agent:notification:jkl012",
                agent_type="notification",
                agent_name="Multi-Channel Notification Agent",
                emergency_id=emergency.id,
                action="Sent alerts to hospital and ambulance crew",
                input_data={
                    "emergency_id": emergency.id,
                    "hospital_contact": "011-2651-5050",
                    "ambulance_id": "AMB-001",
                    "patient_contact": "+91-9876543210"
                },
                output_data={
                    "notifications_sent": 4,
                    "channels": ["SMS", "In-App", "Hospital System", "Ambulance Radio"],
                    "hospital_alerted": True,
                    "ambulance_dispatched": True
                },
                processing_time_ms=234,
                success="SUCCESS"
            )
        ]
        
        for log in logs:
            db.add(log)
        
        db.commit()
        
        print(f"✅ Created {len(logs)} Agent Activity Logs")
        print()
        print("🤖 Agent Execution Timeline:")
        print("=" * 70)
        
        total_time = 0
        for log in logs:
            print(f"✓ {log.agent_name}")
            print(f"  DID: {log.agent_id}")
            print(f"  Action: {log.action}")
            print(f"  Processing Time: {log.processing_time_ms}ms")
            print()
            total_time += log.processing_time_ms
        
        print(f"⚡ Total System Response Time: {total_time}ms ({total_time/1000:.2f} seconds)")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_emergency()
    print("✅ Test emergency data creation complete!")
