import { useQuery } from '@tanstack/react-query';
import { fetchHospitals } from '../services/emergencyService';

/**
 * Hook for fetching available hospitals
 * Automatically refetches every 30 seconds to get updated bed availability
 * 
 * Usage:
 * const { data: hospitals, isLoading, error, refetch } = useHospitals(emergencyId);
 */
export const useHospitals = (emergencyId) => {
  return useQuery({
    queryKey: ['hospitals', emergencyId],
    queryFn: () => fetchHospitals(emergencyId),
    enabled: !!emergencyId, // Only run if emergencyId exists
    refetchInterval: 30000, // Refetch every 30 seconds for Golden Hour updates
    staleTime: 20000, // Consider data stale after 20 seconds
    retry: 3, // Retry 3 times if it fails
    onSuccess: (data) => {
      console.log('🏥 Hospitals updated:', data.length, 'hospitals found');
    },
    onError: (error) => {
      console.error('❌ Failed to fetch hospitals:', error.message);
    },
  });
};
