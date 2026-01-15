// src/services/emergencyService.js
import apiClient from "./api";

// ---------- TRIAGE ----------

// Used by EmergencyForm: send full TriageInput payload to /triage
export const triageEmergency = async (formData) => {
  const payload = {
    patientName: formData.patientName,
    age: formData.age,
    gender: formData.gender,
    contact: formData.contact,
    symptoms: formData.symptoms,
    vitals: {
      bloodPressure: formData.bloodPressure,
      heartRate: formData.heartRate,
      oxygenLevel: formData.oxygenLevel,
    },
    location: {
      lat: Number(formData.latitude),
      lng: Number(formData.longitude),
    },
  };

  const response = await apiClient.post("/triage", payload);
  return response.data;
};

// ---------- STATUS ----------

// Single status check
export const getEmergencyStatus = async (emergencyId) => {
  const response = await apiClient.get(`/status/${emergencyId}`);
  return response.data;
};

// Poll status until hospital is assigned (optional helper)
export const pollEmergencyStatus = async (emergencyId, maxAttempts = 30) => {
  let attempts = 0;

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const checkStatus = async () => {
    try {
      const response = await apiClient.get(`/status/${emergencyId}`);
      const statusData = response.data;

      console.log("📊 Status check:", statusData);

      if (statusData.status === "ASSIGNED" || statusData.assignedHospital) {
        return statusData;
      }

      attempts += 1;
      if (attempts < maxAttempts) {
        await sleep(2000);
        return await checkStatus();
      }
      throw new Error("Hospital assignment timeout");
    } catch (error) {
      console.error("❌ Status polling error:", error);
      attempts += 1;
      if (attempts < maxAttempts) {
        await sleep(2000);
        return await checkStatus();
      }
      throw error;
    }
  };

  return checkStatus();
};

// ---------- HOSPITALS ----------

// List of hospitals with distance/ETA
export const getHospitalsForEmergency = async (emergencyId) => {
  const response = await apiClient.get(`/hospitals/${emergencyId}`);
  return response.data;
};

// Selected / nearest hospital
export const getSelectedHospital = async (emergencyId) => {
  const response = await apiClient.get(`/hospitals/${emergencyId}/selected`);
  return response.data;
};

// Legacy alias if some code still uses this name
export const getHospitalForEmergency = getHospitalsForEmergency;

// ---------- AMBULANCE ----------

export const getAmbulanceLocation = async (emergencyId) => {
  const response = await apiClient.get(`/ambulance/${emergencyId}`);
  return response.data;
};

// ---------- NOTIFY ----------

// Supports both notifyHospital({ hospitalId, emergencyId }) and notifyHospital(hospitalId, emergencyId)
export const notifyHospital = async (payloadOrHospitalId, emergencyId) => {
  let payload = payloadOrHospitalId;

  if (
    typeof payloadOrHospitalId === "number" &&
    typeof emergencyId !== "undefined"
  ) {
    payload = {
      hospitalId: payloadOrHospitalId,
      emergencyId,
    };
  }

  const response = await apiClient.post("/notify", payload);
  return response.data;
};
