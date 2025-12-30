from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Import orchestrator ONLY
from src.orchestrator.orchestrator import orchestrator

router = APIRouter()

# =====================
# Request Models
# =====================

class LocationData(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)

class Vitals(BaseModel):
    bloodPressure: str
    heartRate: int
    oxygenLevel: int

class TriageRequest(BaseModel):
    """Frontend emergency form data"""
    patientName: str
    age: int
    vitals: Vitals
    symptoms: str
    location: LocationData

class EmergencyRequest(BaseModel):
    location: LocationData
    symptoms: List[str]
    vitals: dict
    age: int
    description: str
    contact_email: str

# =====================
# Frontend endpoints
# =====================

@router.post("/triage")
async def triage_emergency(request: TriageRequest):
    """Quick triage endpoint for frontend form submission"""
    # You can implement this or keep legacy triage logic
    return {"message": "Triage endpoint active"}

@router.get("/status/{emergency_id}")
async def get_agent_status(emergency_id: str):
    """Get AI agent processing status"""
    return {
        "agentName": "routing_agent",
        "status": "completed",
        "message": f"Successfully processed emergency {emergency_id}",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.post("/notify")
async def notify_hospital(data: dict):
    """Send notification to selected hospital"""
    hospital_id = data.get("hospitalId")
    emergency_id = data.get("emergencyId")
    if not hospital_id or not emergency_id:
        raise HTTPException(status_code=400, detail="Missing hospitalId or emergencyId")
    return {
        "success": True,
        "message": f"Hospital {hospital_id} has been notified about emergency {emergency_id}",
        "confirmationId": f"notify_{datetime.utcnow().timestamp()}"
    }

# =====================
# Main emergency endpoint
# =====================

@router.post("/api/v1/emergency/create")
async def create_emergency(
    request: EmergencyRequest,
    background_tasks: BackgroundTasks
):
    """
    Submit new emergency request.
    Delegates full workflow to Orchestrator.
    """
    return await orchestrator.handle_emergency(request, background_tasks)
