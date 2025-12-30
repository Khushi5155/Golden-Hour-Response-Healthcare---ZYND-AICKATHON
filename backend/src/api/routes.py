from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Import your agents and services
from src.agents.triage_agent import TriageAgent
from src.agents.routing_agent import routing_agent
from src.agents.notification_agent import notification_agent
from src.agents.hospital_agent import hospital_agent
from src.services.maps_service import maps_service
from src.database.db import MOCK_HOSPITALS


router = APIRouter()


# --- Request Models ---
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


class HospitalRequest(BaseModel):
    severity: str
    location: LocationData
    required_specialists: List[str]


# --- Initialize Triage Agent ---
triage_agent = TriageAgent()


# --- NEW ENDPOINTS FOR FRONTEND ---

@router.post("/triage")
async def triage_emergency(request: TriageRequest):
    """Quick triage endpoint for frontend form submission"""
    try:
        # Convert frontend format to agent format
        triage_input = {
            "symptoms": [s.strip() for s in request.symptoms.split(',')],
            "vitals": {
                "blood_pressure": request.vitals.bloodPressure,
                "heart_rate": request.vitals.heartRate,
                "oxygen_level": request.vitals.oxygenLevel
            },
            "age": request.age
        }
        
        # Run triage agent
        triage_result = triage_agent.execute(triage_input)
        
        # Generate emergency ID
        emergency_id = f"emer_{request.patientName.replace(' ', '_').lower()}_{request.age}"
        
        # Return frontend-compatible response
        return {
            "emergencyId": emergency_id,
            "severity": triage_result.get("severity", "medium"),
            "recommendedSpecialty": triage_result.get("recommended_specialists", ["General"])[0] if triage_result.get("recommended_specialists") else "General",
            "estimatedResponseTime": 15
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")


@router.get("/hospitals/{emergency_id}")
async def get_hospitals_by_emergency(emergency_id: str):
    """Get list of available hospitals for a specific emergency"""
    try:
        hospitals = []
        
        for idx, hospital in enumerate(MOCK_HOSPITALS):
            # Extract coordinates from tuple
            lat, lng = hospital["coords"]
            
            # Format for frontend
            formatted_hospital = {
                "id": hospital["id"],
                "name": hospital["name"],
                "location": {
                    "lat": float(lat),
                    "lng": float(lng)
                },
                "distance": round(5.0 + idx * 2.5, 1),  # Mock distance
                "eta": 12 + idx * 5,  # Mock ETA
                "bedsAvailable": hospital["icu_beds_available"] + hospital["emergency_beds_available"],
                "specialties": [spec.replace('_', ' ').title() for spec in hospital["specialists"]],
                "isRecommended": idx == 0  # First hospital is recommended
            }
            
            hospitals.append(formatted_hospital)
        
        return hospitals
        
    except Exception as e:
        print(f"❌ Error in get_hospitals_by_emergency: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to fetch hospitals: {str(e)}")



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
    
    # You can add actual notification logic here
    return {
        "success": True,
        "message": f"Hospital {hospital_id} has been notified about emergency {emergency_id}",
        "confirmationId": f"notify_{datetime.utcnow().timestamp()}"
    }



@router.post("/emergency")
async def create_emergency(request: EmergencyRequest, background_tasks: BackgroundTasks):
    """Full emergency creation with all agents (original endpoint)"""
    try:
        # 1️⃣ Run triage agent
        triage_input = {
            "symptoms": request.symptoms,
            "vitals": request.vitals,
            "age": request.age
        }
        triage_result = triage_agent.execute(triage_input)

        # 2️⃣ Get address
        address = await maps_service.get_location_address(request.location.lat, request.location.lng)
        emergency_coords = (request.location.lat, request.location.lng)

        # 3️⃣ Find best hospital using routing agent
        best_hospital = await routing_agent.find_best_hospital(emergency_coords, MOCK_HOSPITALS)
        if not best_hospital:
            raise HTTPException(status_code=404, detail="No reachable hospitals found")

        # 4️⃣ Find top suitable hospitals using hospital agent
        top_hospitals = await hospital_agent.find_suitable_hospitals(
            severity=triage_result["severity"],
            location=emergency_coords,
            required_specialists=triage_result["recommended_specialists"],
            hospital_db=MOCK_HOSPITALS
        )

        # 5️⃣ Send notifications in background
        emergency_data = {
            "severity": triage_result["severity"],
            "priority": triage_result["priority"],
            "description": request.description,
            "address": address,
            "contact_email": request.contact_email
        }
        background_tasks.add_task(notification_agent.send_emergency_alert, emergency_data, best_hospital)

        # 6️⃣ Return full response
        return {
            "status": "success",
            "triage_result": triage_result,
            "assigned_hospital": best_hospital["name"],
            "eta_minutes": best_hospital["route_info"]["duration_min"],
            "top_hospitals": top_hospitals,
            "detected_address": address
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emergency creation failed: {str(e)}")


@router.post("/hospitals")
async def get_hospitals(request: HospitalRequest):
    """Direct hospital query endpoint (original)"""
    try:
        location_tuple = (request.location.lat, request.location.lng)
        
        suitable_hospitals = await hospital_agent.find_suitable_hospitals(
            severity=request.severity,
            location=location_tuple,
            required_specialists=request.required_specialists,
            hospital_db=MOCK_HOSPITALS
        )
        
        return {"hospitals": suitable_hospitals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hospital query failed: {str(e)}")
