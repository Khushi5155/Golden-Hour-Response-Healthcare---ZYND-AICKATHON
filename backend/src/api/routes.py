from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
import math
import random


# Import schemas and orchestrator
from src.models.schemas import TriageInput, EmergencyRequest, LocationData
from src.orchestrator.orchestrator import orchestrator
from src.database.db import get_db, Emergency


router = APIRouter()



# =====================
# Distance Calculation Helper Functions
# =====================


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return round(distance, 1)



def calculate_eta(distance_km: float) -> int:
    """
    Calculate estimated time of arrival in minutes
    Assumes average emergency vehicle speed of 40 km/h in Delhi traffic
    """
    avg_speed_kmh = 40  # Emergency vehicle speed in Delhi
    time_hours = distance_km / avg_speed_kmh
    time_minutes = int(time_hours * 60)
    return max(time_minutes, 5)  # Minimum 5 minutes



# =====================
# Frontend Triage Endpoint (NEW - matches your form)
# =====================


@router.post("/triage")
async def triage_emergency(
    request: TriageInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receives emergency from new frontend form.
    Saves to DB and triggers orchestrator.
    """
    print(f"🚨 Received Emergency: {request.patientName}")
    print(f"   Age: {request.age}, Gender: {request.gender}")
    print(f"   Symptoms: {request.symptoms}")
    print(f"   Location: ({request.location.lat}, {request.location.lng})")
    
    try:
        # Create database entry
        emergency = Emergency(
            location=f"Lat: {request.location.lat}, Lng: {request.location.lng}",
            latitude=request.location.lat,
            longitude=request.location.lng,
            symptoms=[request.symptoms],  # Store as JSON array
            age_group=request.age,  # "40-45" format
            vitals={
                "bloodPressure": request.vitals.bloodPressure,
                "heartRate": request.vitals.heartRate,
                "oxygenLevel": request.vitals.oxygenLevel
            },
            status="REGISTERED"
        )
        
        db.add(emergency)
        db.commit()
        db.refresh(emergency)
        
        print(f"✅ Emergency saved with ID: {emergency.id}")
        
        # Prepare payload for orchestrator
        payload = {
            "patientName": request.patientName,
            "age": request.age,
            "gender": request.gender,
            "contact": request.contact,
            "symptoms": request.symptoms,
            "vitals": request.vitals.dict(),
            "location": {"lat": request.location.lat, "lng": request.location.lng}
        }
        
        # Trigger orchestrator in background - FIXED: pass as positional args
        background_tasks.add_task(
            orchestrator.handle_emergency,
            emergency.id,  # First positional argument
            payload        # Second positional argument
        )
        
        return {
            "success": True,
            "emergencyId": emergency.id,
            "message": "Emergency registered successfully",
            "status": "PROCESSING",
            "location": {"lat": request.location.lat, "lng": request.location.lng}
        }
        
    except Exception as e:
        print(f"❌ Error in /triage: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# =====================
# Hospital Endpoint (UPDATED - Real Distance Calculation)
# =====================


@router.get("/hospitals/{emergency_id}")
async def get_hospital_for_emergency(
    emergency_id: int,
    db: Session = Depends(get_db)
):
    """
    Get assigned hospital for an emergency with calculated distances
    """
    try:
        print(f"🏥 Fetching hospitals for Emergency ID: {emergency_id}")
        
        # Fetch emergency from database
        emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
        
        if not emergency:
            raise HTTPException(status_code=404, detail="Emergency not found")
        
        # Get user's location
        user_lat = emergency.latitude
        user_lng = emergency.longitude
        
        print(f"📍 User location: ({user_lat}, {user_lng})")
        
        # Update emergency status if still registered
        if emergency.status == "REGISTERED":
            emergency.status = "ASSIGNED"
            emergency.severity = "HIGH"
            db.commit()
            db.refresh(emergency)
            print(f"✅ Updated emergency status to ASSIGNED")
        
        # Hospital coordinates (actual locations in Delhi/NCR)
        hospitals_data = [
            {
                "id": 1,
                "name": "All India Institute of Medical Sciences (AIIMS)",
                "address": "Ansari Nagar, New Delhi - 110029",
                "lat": 28.5672,
                "lng": 77.2100,
                "phone": "+91-11-2658-8500",
                "specialties": ["Emergency Medicine", "Cardiology", "Trauma", "ICU"],
                "bedsAvailable": 15
            },
            {
                "id": 2,
                "name": "Fortis Hospital",
                "address": "Sector 62, Noida, Uttar Pradesh",
                "lat": 28.6066,
                "lng": 77.3572,
                "phone": "+91-120-500-3333",
                "specialties": ["Emergency Medicine", "Neurology", "Orthopedics"],
                "bedsAvailable": 10
            },
            {
                "id": 3,
                "name": "Max Super Specialty Hospital",
                "address": "Saket, New Delhi - 110017",
                "lat": 28.5244,
                "lng": 77.2066,
                "phone": "+91-11-2651-5050",
                "specialties": ["Emergency Medicine", "General Surgery", "ICU"],
                "bedsAvailable": 8
            },
            {
                "id": 4,
                "name": "Apollo Hospital",
                "address": "Mathura Road, Sarita Vihar, Delhi",
                "lat": 28.5355,
                "lng": 77.2952,
                "phone": "+91-11-2692-5858",
                "specialties": ["Emergency Medicine", "Cardiology", "Pulmonology"],
                "bedsAvailable": 6
            },
            {
                "id": 5,
                "name": "Safdarjung Hospital",
                "address": "Ring Road, New Delhi - 110029",
                "lat": 28.5678,
                "lng": 77.2065,
                "phone": "+91-11-2673-0000",
                "specialties": ["Emergency Medicine", "Trauma", "General Medicine"],
                "bedsAvailable": 12
            },
            {
                "id": 6,
                "name": "Fortis Hospital Shalimar Bagh",
                "address": "A Block, Shalimar Bagh, Delhi - 110088",
                "lat": 28.7194,
                "lng": 77.1642,
                "phone": "+91-11-4714-4444",
                "specialties": ["Emergency Medicine", "Cardiology", "Orthopedics"],
                "bedsAvailable": 9
            },
            {
                "id": 7,
                "name": "Batra Hospital",
                "address": "Tughlakabad, New Delhi - 110062",
                "lat": 28.5005,
                "lng": 77.2806,
                "phone": "+91-11-2995-5555",
                "specialties": ["Emergency Medicine", "Cardiology", "Neurology"],
                "bedsAvailable": 7
            },
            {
                "id": 8,
                "name": "Max Hospital Pitampura",
                "address": "Pitampura, Delhi - 110034",
                "lat": 28.6952,
                "lng": 77.1312,
                "phone": "+91-11-4040-4040",
                "specialties": ["Emergency Medicine", "Neurology", "Orthopedics"],
                "bedsAvailable": 11
            }
        ]
        
        # Calculate distance and ETA for each hospital
        hospitals_with_distance = []
        for hospital in hospitals_data:
            distance = calculate_distance(user_lat, user_lng, hospital["lat"], hospital["lng"])
            eta = calculate_eta(distance)
            
            hospitals_with_distance.append({
                "id": hospital["id"],
                "name": hospital["name"],
                "address": hospital["address"],
                "distance": distance,
                "eta": eta,
                "bedsAvailable": hospital["bedsAvailable"],
                "phone": hospital["phone"],
                "specialties": hospital["specialties"],
                "isRecommended": False  # Will be set for nearest hospital
            })
        
        # Sort by distance (nearest first)
        hospitals_with_distance.sort(key=lambda x: x["distance"])
        
        # Mark nearest hospital as recommended
        if hospitals_with_distance:
            hospitals_with_distance[0]["isRecommended"] = True
            
            # Update emergency with nearest hospital info
            emergency.assigned_hospital_id = hospitals_with_distance[0]["id"]
            emergency.estimated_arrival_time = f"{hospitals_with_distance[0]['eta']} minutes"
            db.commit()
        
        print(f"✅ Returning {len(hospitals_with_distance)} hospitals sorted by distance")
        print(f"   Nearest: {hospitals_with_distance[0]['name']} ({hospitals_with_distance[0]['distance']} km, {hospitals_with_distance[0]['eta']} min)")
        
        return {
            "emergencyId": emergency_id,
            "status": "assigned",
            "hospitals": hospitals_with_distance,
            "message": f"Found {len(hospitals_with_distance)} nearby hospitals"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching hospitals: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# =====================
# Ambulance Tracking Endpoints
# =====================


@router.get("/ambulance/{emergency_id}")
async def get_ambulance_location(
    emergency_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current ambulance location for an emergency.
    Simulates real-time ambulance tracking.
    """
    try:
        print(f"🚑 Fetching ambulance location for Emergency ID: {emergency_id}")
        
        # Fetch emergency from database
        emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
        
        if not emergency:
            raise HTTPException(status_code=404, detail="Emergency not found")
        
        user_lat = emergency.latitude
        user_lng = emergency.longitude
        
        # Simulate ambulance starting position (nearby but not at emergency location)
        # In production, this would come from actual GPS tracking
        ambulance_lat = user_lat + random.uniform(-0.02, 0.02)  # ~2km radius
        ambulance_lng = user_lng + random.uniform(-0.02, 0.02)
        
        # Calculate distance from ambulance to emergency
        distance_to_emergency = calculate_distance(ambulance_lat, ambulance_lng, user_lat, user_lng)
        eta_minutes = calculate_eta(distance_to_emergency)
        
        # Determine status based on distance
        if distance_to_emergency < 0.5:
            status = "arriving"
        elif distance_to_emergency < 2:
            status = "nearby"
        else:
            status = "en_route"
        
        print(f"✅ Ambulance at ({ambulance_lat}, {ambulance_lng})")
        print(f"   Distance to emergency: {distance_to_emergency} km, ETA: {eta_minutes} min")
        
        return {
            "emergencyId": emergency_id,
            "ambulanceId": f"AMB-{emergency_id:04d}",
            "currentLat": round(ambulance_lat, 6),
            "currentLng": round(ambulance_lng, 6),
            "status": status,
            "distanceToEmergency": distance_to_emergency,
            "eta": f"{eta_minutes} minutes",
            "driverName": "Ramesh Kumar",
            "vehicleNumber": f"DL-{random.randint(1,9)}C-{random.randint(1000,9999)}",
            "lastUpdated": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching ambulance location: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hospitals/{emergency_id}/selected")
async def get_selected_hospital(
    emergency_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the selected/nearest hospital for an emergency.
    Returns single hospital with full details for map display.
    """
    try:
        print(f"🏥 Fetching selected hospital for Emergency ID: {emergency_id}")
        
        # Fetch emergency from database
        emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
        
        if not emergency:
            raise HTTPException(status_code=404, detail="Emergency not found")
        
        user_lat = emergency.latitude
        user_lng = emergency.longitude
        
        # Get nearest hospital (reuse hospital data from get_hospital_for_emergency)
        hospitals_data = [
            {
                "id": 1,
                "name": "AIIMS Delhi",
                "address": "Ansari Nagar, New Delhi - 110029",
                "lat": 28.5672,
                "lng": 77.2100,
                "phone": "+91-11-2658-8500"
            },
            {
                "id": 2,
                "name": "Fortis Hospital Noida",
                "address": "Sector 62, Noida",
                "lat": 28.6066,
                "lng": 77.3572,
                "phone": "+91-120-500-3333"
            },
            {
                "id": 3,
                "name": "Max Hospital Saket",
                "address": "Saket, New Delhi",
                "lat": 28.5244,
                "lng": 77.2066,
                "phone": "+91-11-2651-5050"
            },
            {
                "id": 4,
                "name": "Apollo Hospital Delhi",
                "address": "Sarita Vihar, Delhi",
                "lat": 28.5355,
                "lng": 77.2952,
                "phone": "+91-11-2692-5858"
            }
        ]
        
        # Calculate distances and find nearest
        nearest_hospital = None
        min_distance = float('inf')
        
        for hospital in hospitals_data:
            distance = calculate_distance(user_lat, user_lng, hospital["lat"], hospital["lng"])
            if distance < min_distance:
                min_distance = distance
                nearest_hospital = hospital
        
        if not nearest_hospital:
            raise HTTPException(status_code=404, detail="No hospitals found")
        
        eta_minutes = calculate_eta(min_distance)
        
        # Update emergency record with selected hospital
        emergency.assigned_hospital_id = nearest_hospital["id"]
        emergency.estimated_arrival_time = f"{eta_minutes} minutes"
        db.commit()
        
        print(f"✅ Selected Hospital: {nearest_hospital['name']}")
        print(f"   Distance: {min_distance} km, ETA: {eta_minutes} min")
        
        return {
            "emergencyId": emergency_id,
            "hospitalId": nearest_hospital["id"],
            "name": nearest_hospital["name"],
            "address": nearest_hospital["address"],
            "latitude": nearest_hospital["lat"],
            "longitude": nearest_hospital["lng"],
            "phone": nearest_hospital["phone"],
            "distance": round(min_distance, 1),
            "eta": f"{eta_minutes} minutes",
            "bedsAvailable": random.randint(5, 15),
            "isSelected": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching selected hospital: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# =====================
# Supporting Endpoints
# =====================


@router.get("/status/{emergency_id}")
async def get_agent_status(emergency_id: int, db: Session = Depends(get_db)):
    """Get emergency processing status"""
    print(f"📊 Status check for Emergency ID: {emergency_id}")
    
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    
    # Auto-update status if still registered (simulate processing)
    if emergency.status == "REGISTERED":
        emergency.status = "PROCESSING"
        emergency.severity = "HIGH"
        db.commit()
        db.refresh(emergency)
        print(f"✅ Updated status to PROCESSING")
    
    return {
        "emergencyId": emergency.id,
        "status": emergency.status,
        "severity": emergency.severity,
        "assignedHospital": emergency.assigned_hospital_id,
        "eta": emergency.estimated_arrival_time,
        "timestamp": emergency.created_at.isoformat() if emergency.created_at else None
    }



@router.post("/notify")
async def notify_hospital(data: dict):
    """Send notification to selected hospital"""
    hospital_id = data.get("hospitalId")
    emergency_id = data.get("emergencyId")
    
    if not hospital_id or not emergency_id:
        raise HTTPException(status_code=400, detail="Missing hospitalId or emergencyId")
    
    print(f"📢 Notifying Hospital {hospital_id} about Emergency {emergency_id}")
    
    return {
        "success": True,
        "message": f"Hospital {hospital_id} notified about emergency {emergency_id}",
        "confirmationId": f"notify_{int(datetime.utcnow().timestamp())}"
    }



# =====================
# Legacy Endpoint (Backward compatibility)
# =====================


@router.post("/emergency/create")
async def create_emergency(
    request: EmergencyRequest,
    background_tasks: BackgroundTasks
):
    """
    Legacy endpoint - kept for backward compatibility.
    Use /triage for new frontend.
    """
    return await orchestrator.handle_emergency(request, background_tasks)
