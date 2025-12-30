import { useQuery } from '@tanstack/react-query';
import { getAgentStatus } from '../services/emergencyService';

/**
 * Hook for tracking AI agent processing status
 * Shows what agents are doing in real-time
 * 
 * Usage:
 * const { data: agentStatus, isLoading } = useAgentStatus(emergencyId);
 */
export const useAgentStatus = (emergencyId) => {
  return useQuery({
    queryKey: ['agentStatus', emergencyId],
    queryFn: () => getAgentStatus(emergencyId),
    enabled: !!emergencyId,
    refetchInterval: 5000, // Check agent status every 5 seconds
    staleTime: 4000,
    retry: 2,
    onSuccess: (data) => {
      console.log('🤖 Agent status updated:', data);
    },
  });
};
