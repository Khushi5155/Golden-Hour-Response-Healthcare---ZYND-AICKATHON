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

// Get current status of emergency
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

// NEW: Poll emergency status with retry logic
export const pollEmergencyStatus = async (emergencyId, maxAttempts = 30) => {
  let attempts = 0;

  const checkStatus = async () => {
    try {
      const response = await apiClient.get(`/status/${emergencyId}`);
      const statusData = response.data;

      console.log('📊 Status check:', statusData);

      // Check if hospital is assigned
      if (statusData.status === 'ASSIGNED' || statusData.assignedHospital) {
        return statusData;
      }

      // Continue polling if not assigned yet
      attempts++;
      if (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
        return await checkStatus(); // Recursive call
      } else {
        throw new Error('Hospital assignment timeout');
      }

    } catch (error) {
      console.error('❌ Status polling error:', error);
      attempts++;
      
      if (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000));
        return await checkStatus();
      } else {
        throw error;
      }
    }
  };

  return await checkStatus();
};

// NEW: Get emergency status (single check, no polling)
export const getEmergencyStatus = async (emergencyId) => {
  const response = await apiClient.get(`/status/${emergencyId}`);
  return response.data;
};

// NEW: Get hospital details for emergency
export const getHospitalForEmergency = async (emergencyId) => {
  const response = await apiClient.get(`/hospitals/${emergencyId}`);
  return response.data;
};
