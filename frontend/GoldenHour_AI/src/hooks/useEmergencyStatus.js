import { useQuery } from '@tanstack/react-query';
import { getEmergencyStatus, getHospitalForEmergency } from '../services/emergencyService';

/**
 * Hook for polling emergency status and fetching hospital when assigned
 * 
 * Usage:
 * const { data, isLoading, error } = useEmergencyStatus(emergencyId, {
 *   enabled: !!emergencyId,
 *   onHospitalAssigned: (data) => console.log('Hospital assigned:', data)
 * });
 */
export const useEmergencyStatus = (emergencyId, options = {}) => {
  const { enabled = true, onHospitalAssigned } = options;

  return useQuery({
    queryKey: ['emergencyStatus', emergencyId],
    queryFn: async () => {
      // Get current status
      const status = await getEmergencyStatus(emergencyId);
      
      console.log('📊 Polling status:', status);
      
      // If hospital is assigned, fetch hospital details
      if ((status.status === 'ASSIGNED' || status.assignedHospital) && !status.hospital) {
        try {
          const hospitalData = await getHospitalForEmergency(emergencyId);
          
          // Merge hospital data into status
          const fullData = {
            ...status,
            hospital: hospitalData.hospital || hospitalData
          };
          
          // Trigger callback if provided
          if (onHospitalAssigned) {
            onHospitalAssigned(fullData);
          }
          
          return fullData;
        } catch (error) {
          console.error('❌ Failed to fetch hospital:', error);
          // Return status without hospital if fetch fails
          return status;
        }
      }
      
      return status;
    },
    enabled: enabled && !!emergencyId,
    refetchInterval: (query) => {
      const data = query.state.data;
      
      // Stop polling if hospital is assigned
      if (data?.assignedHospital || data?.status === 'ASSIGNED' || data?.hospital) {
        console.log('✅ Hospital assigned, stopping polling');
        return false;
      }
      
      // Poll every 2 seconds while waiting
      return 2000;
    },
    retry: 3,
    retryDelay: 1000,
    staleTime: 0, // Always fetch fresh data
  });
};
