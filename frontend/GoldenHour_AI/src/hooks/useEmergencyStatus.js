import { useQuery } from '@tanstack/react-query';
import {
  getEmergencyStatus,
  getHospitalForEmergency,
} from '../services/emergencyService';

/**
 * Hook for polling emergency status and fetching hospital when assigned.
 *
 * Usage:
 * const { data, isLoading, error } = useEmergencyStatus(emergencyId, {
 *   enabled: !!emergencyId,
 *   onHospitalAssigned: (data) => console.log('Hospital assigned:', data),
 * });
 */
export const useEmergencyStatus = (emergencyId, options = {}) => {
  const { enabled = true, onHospitalAssigned } = options;

  return useQuery({
    queryKey: ['emergencyStatus', emergencyId],
    queryFn: async () => {
      const status = await getEmergencyStatus(emergencyId);

      console.log('📊 Polling status:', status);

      if (
        (status.status === 'ASSIGNED' || status.assignedHospital) &&
        !status.hospital
      ) {
        try {
          const hospitalData = await getHospitalForEmergency(emergencyId);

          const fullData = {
            ...status,
            hospital: hospitalData.hospital || hospitalData,
          };

          if (onHospitalAssigned) {
            onHospitalAssigned(fullData);
          }

          return fullData;
        } catch (error) {
          console.error('❌ Failed to fetch hospital:', error);
          return status;
        }
      }

      return status;
    },
    enabled: enabled && !!emergencyId,
    refetchInterval: (query) => {
      const data = query.state.data;

      if (
        data?.assignedHospital ||
        data?.status === 'ASSIGNED' ||
        data?.hospital
      ) {
        console.log('✅ Hospital assigned, stopping polling');
        return false;
      }

      return 2000; // poll every 2s until assigned
    },
    retry: 3,
    retryDelay: 1000,
    staleTime: 0,
  });
};
