from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class LocationData(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class Vitals(BaseModel):
    bloodPressure: Optional[str] = None
    heartRate: Optional[int] = Field(None, ge=30, le=200)
    oxygenLevel: Optional[int] = Field(None, ge=50, le=100)


class TriageInput(BaseModel):
    """Schema matching the new frontend form"""
    patientName: str
    age: str  # Changed from int to str (e.g., "40-45")
    gender: str
    contact: str
    vitals: Vitals
    symptoms: str  # Changed from List[str] to str
    location: LocationData


class EmergencyRequest(BaseModel):
    """Legacy schema for backward compatibility"""
    location: LocationData
    symptoms: List[str]
    vitals: dict
    age: int
    description: str
    contact_email: str
