import { useQuery } from '@tanstack/react-query';
import { getAmbulanceLocation, getSelectedHospital } from '../services/emergencyService';

/**
 * Live ambulance tracking using backend /ambulance/{id}.
 */
export function useAmbulanceTracking(emergencyId) {
  return useQuery({
    queryKey: ['ambulance', emergencyId],
    queryFn: async () => {
      if (!emergencyId) return null;
      return await getAmbulanceLocation(emergencyId);
    },
    enabled: !!emergencyId,
    refetchInterval: 5000, // poll every 5s
    staleTime: 0,
  });
}

/**
 * Selected/nearest hospital using /hospitals/{id}/selected.
 */
export function useSelectedHospital(emergencyId) {
  return useQuery({
    queryKey: ['selectedHospital', emergencyId],
    queryFn: async () => {
      if (!emergencyId) return null;
      return await getSelectedHospital(emergencyId);
    },
    enabled: !!emergencyId,
    staleTime: 30000,
  });
}
