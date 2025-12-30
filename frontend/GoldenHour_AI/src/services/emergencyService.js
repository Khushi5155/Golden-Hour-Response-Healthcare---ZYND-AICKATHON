import apiClient from './api';

// Submit new emergency to triage agent
export const triageEmergency = async (emergencyData) => {
  const response = await apiClient.post('/triage', emergencyData);
  return response.data;
};

// Get list of available hospitals
export const fetchHospitals = async (emergencyId) => {
  const response = await apiClient.get(`/hospitals/${emergencyId}`);
  return response.data;
};

// Get current status of all agents
export const getAgentStatus = async (emergencyId) => {
  const response = await apiClient.get(`/status/${emergencyId}`);
  return response.data;
};

// Send notification to hospital
export const notifyHospital = async (hospitalId, emergencyId) => {
  const response = await apiClient.post('/notify', {
    hospitalId,
    emergencyId
  });
  return response.data;
};
