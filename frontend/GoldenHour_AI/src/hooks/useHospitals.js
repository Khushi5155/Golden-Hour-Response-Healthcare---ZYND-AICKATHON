// src/hooks/useHospitals.js
import { useQuery } from '@tanstack/react-query';
import { getHospitalsForEmergency } from '../services/emergencyService';

/**
 * Hook for fetching available hospitals
 * Automatically refetches every 30 seconds to get updated bed availability
 *
 * Usage:
 * const { data, isLoading, error, refetch } = useHospitals(emergencyId);
 * data => { emergencyId, status, hospitals: [...] }
 */
export const useHospitals = (emergencyId) => {
  return useQuery({
    queryKey: ['hospitals', emergencyId],
    queryFn: () => getHospitalsForEmergency(emergencyId),
    enabled: !!emergencyId, // Only run if emergencyId exists
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 20000,
    retry: 3,
    onSuccess: (data) => {
      const count = Array.isArray(data?.hospitals) ? data.hospitals.length : 0;
      console.log('🏥 Hospitals updated:', count, 'hospitals found');
    },
    onError: (error) => {
      console.error('❌ Failed to fetch hospitals:', error.message);
    },
  });
};
