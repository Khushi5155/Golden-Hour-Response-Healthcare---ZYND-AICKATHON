from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

# Import schemas and orchestrator
from src.models.schemas import TriageInput, EmergencyRequest, LocationData
from src.orchestrator.orchestrator import orchestrator
from src.database.db import get_db, Emergency

router = APIRouter()


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
            "status": "PROCESSING"
        }
        
    except Exception as e:
        print(f"❌ Error in /triage: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =====================
# Hospital Endpoint (UPDATED - Returns Mock Hospital Data)
# =====================

@router.get("/hospitals/{emergency_id}")
async def get_hospital_for_emergency(
    emergency_id: int,
    db: Session = Depends(get_db)
):
    """
    Get assigned hospital for an emergency
    """
    try:
        print(f"🏥 Fetching hospitals for Emergency ID: {emergency_id}")
        
        # Fetch emergency from database
        emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
        
        if not emergency:
            raise HTTPException(status_code=404, detail="Emergency not found")
        
        # Update emergency status if still registered
        if emergency.status == "REGISTERED":
            emergency.status = "ASSIGNED"
            emergency.severity = "HIGH"
            emergency.assigned_hospital_id = 1
            emergency.estimated_arrival_time = "12 minutes"
            db.commit()
            db.refresh(emergency)
            print(f"✅ Updated emergency status to ASSIGNED")
        
        # MOCK DATA FOR TESTING - Replace with real hospital query later
        mock_hospitals = [
            {
                "id": 1,
                "name": "All India Institute of Medical Sciences (AIIMS)",
                "address": "Ansari Nagar, New Delhi - 110029",
                "distance": 3.2,
                "eta": 12,
                "bedsAvailable": 15,
                "phone": "+91-11-2658-8500",
                "specialties": ["Emergency Medicine", "Cardiology", "Trauma", "ICU"],
                "isRecommended": True
            },
            {
                "id": 2,
                "name": "Fortis Hospital",
                "address": "Sector 62, Noida, Uttar Pradesh",
                "distance": 5.8,
                "eta": 18,
                "bedsAvailable": 10,
                "phone": "+91-120-500-3333",
                "specialties": ["Emergency Medicine", "Neurology", "Orthopedics"],
                "isRecommended": False
            },
            {
                "id": 3,
                "name": "Max Super Specialty Hospital",
                "address": "Saket, New Delhi - 110017",
                "distance": 7.5,
                "eta": 25,
                "bedsAvailable": 8,
                "phone": "+91-11-2651-5050",
                "specialties": ["Emergency Medicine", "General Surgery", "ICU"],
                "isRecommended": False
            },
            {
                "id": 4,
                "name": "Apollo Hospital",
                "address": "Mathura Road, Sarita Vihar, Delhi",
                "distance": 9.2,
                "eta": 30,
                "bedsAvailable": 6,
                "phone": "+91-11-2692-5858",
                "specialties": ["Emergency Medicine", "Cardiology", "Pulmonology"],
                "isRecommended": False
            },
            {
                "id": 5,
                "name": "Safdarjung Hospital",
                "address": "Ring Road, New Delhi - 110029",
                "distance": 4.5,
                "eta": 15,
                "bedsAvailable": 12,
                "phone": "+91-11-2673-0000",
                "specialties": ["Emergency Medicine", "Trauma", "General Medicine"],
                "isRecommended": False
            }
        ]
        
        print(f"✅ Returning {len(mock_hospitals)} hospitals for Emergency {emergency_id}")
        
        return {
            "emergencyId": emergency_id,
            "status": "assigned",
            "hospitals": mock_hospitals,
            "message": "Showing nearby hospitals (Mock data for testing)"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching hospitals: {e}")
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
