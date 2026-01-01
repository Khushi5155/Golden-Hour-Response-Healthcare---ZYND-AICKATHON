import { useMutation } from '@tanstack/react-query';
import { triageEmergency } from '../services/emergencyService';

/**
 * Hook for submitting emergency triage requests
 * Will use this when the form is submitted
 * 
 * Usage:
 * const { mutate: submitEmergency, data, isLoading, error } = useTriageEmergency();
 * submitEmergency(formData);
 */
export const useTriageEmergency = () => {
  return useMutation({
    mutationFn: (emergencyData) => triageEmergency(emergencyData),
    onSuccess: (data) => {
      console.log('✅ Triage successful:', data);
      
      // Store emergency ID for future requests
      if (data?.emergencyId) {
        localStorage.setItem('currentEmergencyId', data.emergencyId);
        console.log('📝 Stored Emergency ID:', data.emergencyId);
      }
      
      // Return data for component to use
      return data;
    },
    onError: (error) => {
      console.error('❌ Triage failed:', error.message);
      // Can display this error in the UI
    },
  });
};
