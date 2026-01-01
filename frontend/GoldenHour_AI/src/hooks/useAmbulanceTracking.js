import { useQuery } from '@tanstack/react-query';

const API_BASE_URL = 'http://localhost:8000/api';

export function useAmbulanceTracking(emergencyId) {
  return useQuery({
    queryKey: ['ambulance', emergencyId],
    queryFn: async () => {
      if (!emergencyId) return null;
      
      const response = await fetch(`${API_BASE_URL}/ambulance/${emergencyId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch ambulance data');
      }
      return response.json();
    },
    enabled: !!emergencyId,
    refetchInterval: 5000,
    staleTime: 0,
  });
}

export function useSelectedHospital(emergencyId) {
  return useQuery({
    queryKey: ['selectedHospital', emergencyId],
    queryFn: async () => {
      if (!emergencyId) return null;
      
      const response = await fetch(`${API_BASE_URL}/hospitals/${emergencyId}/selected`);
      if (!response.ok) {
        throw new Error('Failed to fetch hospital data');
      }
      return response.json();
    },
    enabled: !!emergencyId,
    staleTime: 30000,
  });
}
