import { useQuery } from '@tanstack/react-query';
import { getEmergencyStatus } from '../services/emergencyService';

/**
 * Hook for tracking AI agent processing status.
 *
 * Usage:
 * const { data: agentStatus, isLoading } = useAgentStatus(emergencyId);
 */
export const useAgentStatus = (emergencyId) => {
  return useQuery({
    queryKey: ['agentStatus', emergencyId],
    queryFn: () => getEmergencyStatus(emergencyId),
    enabled: !!emergencyId,
    refetchInterval: 5000, // every 5s
    staleTime: 4000,
    retry: 2,
    onSuccess: (data) => {
      console.log('🤖 Agent status updated:', data);
    },
  });
};
