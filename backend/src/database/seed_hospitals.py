import os
import sys

# Fix import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database.db import SessionLocal, Hospital

# Your hospital data
HOSPITALS = [
    {
        "id": "max_hospital_saket",
        "name": "Max Hospital, Saket",
        "address": "Press Enclave Road, Saket, New Delhi",
        "latitude": 28.5245,
        "longitude": 77.2060,
        "icu_beds_available": 5,
        "icu_beds_total": 15,
        "general_beds_available": 10,
        "general_beds_total": 30,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "phone": "011-2651-5050"
    },
    {
        "id": "aiims_trauma_center",
        "name": "AIIMS Trauma Center",
        "address": "Ansari Nagar, New Delhi",
        "latitude": 28.5650,
        "longitude": 77.2060,
        "icu_beds_available": 2,
        "icu_beds_total": 10,
        "general_beds_available": 5,
        "general_beds_total": 20,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "has_neurosurgeon": "true",
        "phone": "011-2658-8500"
    },
    {
        "id": "city_general",
        "name": "City General Hospital",
        "address": "Rohini, New Delhi",
        "latitude": 28.7041,
        "longitude": 77.1025,
        "icu_beds_available": 0,
        "icu_beds_total": 5,
        "general_beds_available": 5,
        "general_beds_total": 25,
        "has_cardiologist": "false",
        "has_trauma_center": "false",
        "phone": "011-2745-0000"
    },
    {
        "id": "apollo_hospital",
        "name": "Apollo Hospital, Delhi",
        "address": "Sarita Vihar, New Delhi",
        "latitude": 28.5672,
        "longitude": 77.2100,
        "icu_beds_available": 10,
        "icu_beds_total": 25,
        "general_beds_available": 15,
        "general_beds_total": 50,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "has_neurosurgeon": "true",
        "phone": "011-2692-5858"
    },
    {
        "id": "fortis_escorts",
        "name": "Fortis Escorts Heart Institute",
        "address": "Okhla Road, New Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "icu_beds_available": 15,
        "icu_beds_total": 35,
        "general_beds_available": 20,
        "general_beds_total": 60,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "phone": "011-4713-5000"
    },
    {
        "id": "blk_super_speciality",
        "name": "BLK Super Speciality Hospital",
        "address": "Pusa Road, Rajendra Place",
        "latitude": 28.6519,
        "longitude": 77.1890,
        "icu_beds_available": 8,
        "icu_beds_total": 20,
        "general_beds_available": 12,
        "general_beds_total": 40,
        "has_cardiologist": "true",
        "has_trauma_center": "false",
        "phone": "011-3040-3040"
    },
    {
        "id": "sir_ganga_ram",
        "name": "Sir Ganga Ram Hospital",
        "address": "Rajinder Nagar, New Delhi",
        "latitude": 28.6358,
        "longitude": 77.2041,
        "icu_beds_available": 10,
        "icu_beds_total": 22,
        "general_beds_available": 15,
        "general_beds_total": 45,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "phone": "011-2575-0000"
    },
    {
        "id": "indraprastha_apollo",
        "name": "Indraprastha Apollo Hospital",
        "address": "Sarita Vihar, New Delhi",
        "latitude": 28.5610,
        "longitude": 77.2600,
        "icu_beds_available": 12,
        "icu_beds_total": 28,
        "general_beds_available": 18,
        "general_beds_total": 55,
        "has_cardiologist": "true",
        "has_trauma_center": "true",
        "phone": "011-2692-5858"
    },
    {
        "id": "fortis_vasant_kunj",
        "name": "Fortis Vasant Kunj",
        "address": "Sector B, Aruna Asaf Ali Marg",
        "latitude": 28.5390,
        "longitude": 77.1880,
        "icu_beds_available": 8,
        "icu_beds_total": 18,
        "general_beds_available": 12,
        "general_beds_total": 38,
        "has_cardiologist": "false",
        "has_trauma_center": "true",
        "phone": "011-4277-6222"
    },
    {
        "id": "venkateshwar_hospital",
        "name": "Venkateshwar Hospital",
        "address": "Sector 18A, Dwarka, New Delhi",
        "latitude": 28.6110,
        "longitude": 77.2220,
        "icu_beds_available": 6,
        "icu_beds_total": 15,
        "general_beds_available": 10,
        "general_beds_total": 35,
        "has_cardiologist": "false",
        "has_trauma_center": "true",
        "phone": "011-4277-3000"
    }
]


def seed_hospitals():
    """Insert hospital data into database"""
    db = SessionLocal()
    
    print("🌱 Seeding Hospital Data...")
    print()
    
    try:
        # Clear existing data
        deleted = db.query(Hospital).delete()
        if deleted > 0:
            print(f"🗑️  Deleted {deleted} old hospitals")
        
        # Insert new hospitals
        for hospital_data in HOSPITALS:
            hospital = Hospital(**hospital_data)
            db.add(hospital)
        
        db.commit()
        
        print(f"✅ Successfully added {len(HOSPITALS)} hospitals")
        print()
        
        # Verify
        count = db.query(Hospital).count()
        print(f"📊 Total hospitals in database: {count}")
        
        # Show summary
        print()
        print("🏥 Hospital Summary:")
        print("=" * 60)
        
        hospitals = db.query(Hospital).all()
        for h in hospitals:
            icu_icon = "✅" if h.icu_beds_available > 0 else "❌"
            print(f"{icu_icon} {h.name}")
            print(f"   📍 ({h.latitude}, {h.longitude})")
            print(f"   🛏️  ICU: {h.icu_beds_available}/{h.icu_beds_total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_hospitals()
    print()
    print("✅ Hospital seeding complete!")
