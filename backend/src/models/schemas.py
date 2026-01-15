from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class LocationData(BaseModel):
    # Optional coordinates so null / missing is allowed
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)


class Vitals(BaseModel):
    bloodPressure: Optional[str] = None
    heartRate: Optional[int] = Field(None, ge=30, le=200)
    oxygenLevel: Optional[int] = Field(None, ge=50, le=100)


class TriageInput(BaseModel):
    """Schema matching the new frontend form"""
    patientName: str
    age: str          # e.g. "40-45"
    gender: str
    contact: str
    vitals: Vitals
    symptoms: str     # single string from form
    # Make location optional so backend accepts null / absence
    location: Optional[LocationData] = None


class EmergencyRequest(BaseModel):
    """Legacy schema for backward compatibility"""
    location: LocationData
    symptoms: List[str]
    vitals: Dict
    age: int
    description: str
    contact_email: str
