import os
import sys

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database.db import SessionLocal, Emergency, Hospital, AgentLog


def verify_database():
    db = SessionLocal()
    
    print("🔍 DATABASE VERIFICATION")
    print("=" * 70)
    print()
    
    # Count records
    hospitals = db.query(Hospital).count()
    emergencies = db.query(Emergency).count()
    logs = db.query(AgentLog).count()
    
    print(f"📊 Record Counts:")
    print(f"   🏥 Hospitals: {hospitals}")
    print(f"   🚨 Emergencies: {emergencies}")
    print(f"   🤖 Agent Logs: {logs}")
    print()
    
    if emergencies > 0:
        # Get latest emergency
        emergency = db.query(Emergency).order_by(Emergency.id.desc()).first()
        
        print(f"📋 Latest Emergency (ID: {emergency.id}):")
        print("=" * 70)
        print(f"Location: {emergency.location}")
        print(f"Coordinates: ({emergency.latitude}, {emergency.longitude})")
        print(f"Severity: {emergency.severity} (Priority {emergency.priority})")
        print(f"Symptoms: {', '.join(emergency.symptoms)}")
        print(f"Age Group: {emergency.age_group}")
        print(f"Status: {emergency.status}")
        print(f"Created: {emergency.created_at}")
        print()
        
        # Get its agent logs
        emergency_logs = db.query(AgentLog).filter(
            AgentLog.emergency_id == emergency.id
        ).order_by(AgentLog.timestamp).all()
        
        print(f"🤖 Agent Execution Timeline ({len(emergency_logs)} actions):")
        print("=" * 70)
        for log in emergency_logs:
            print(f"✓ [{log.agent_type.upper()}] {log.action}")
            print(f"  DID: {log.agent_id}")
            print(f"  Processing: {log.processing_time_ms}ms | Status: {log.success}")
            print()
    
    # Show hospitals with ICU beds
    icu_hospitals = db.query(Hospital).filter(
        Hospital.icu_beds_available > 0
    ).order_by(Hospital.icu_beds_available.desc()).all()
    
    print(f"🏥 Hospitals with Available ICU Beds ({len(icu_hospitals)}):")
    print("=" * 70)
    for h in icu_hospitals:
        print(f"✓ {h.name}")
        print(f"  ICU: {h.icu_beds_available}/{h.icu_beds_total} | General: {h.general_beds_available}/{h.general_beds_total}")
        print(f"  Cardiologist: {h.has_cardiologist} | Trauma: {h.has_trauma_center}")
    
    db.close()
    print()
    print("✅ Database verification complete!")


if __name__ == "__main__":
    verify_database()
