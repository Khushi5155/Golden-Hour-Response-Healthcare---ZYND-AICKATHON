import { useMutation } from '@tanstack/react-query';
import { notifyHospital } from '../services/emergencyService';

/**
 * Hook for sending notifications to selected hospital
 * 
 * Usage:
 * const { mutate: notify, isLoading } = useNotifyHospital();
 * notify({ hospitalId: 'hosp_001', emergencyId: 'emer_123' });
 */
export const useNotifyHospital = () => {
  return useMutation({
    mutationFn: ({ hospitalId, emergencyId }) => 
      notifyHospital(hospitalId, emergencyId),
    onSuccess: (data) => {
      console.log('📢 Hospital notified successfully:', data);
      alert('Hospital has been notified! ETA confirmed.');
    },
    onError: (error) => {
      console.error('❌ Notification failed:', error.message);
      alert('Failed to notify hospital. Please try again.');
    },
  });
};
