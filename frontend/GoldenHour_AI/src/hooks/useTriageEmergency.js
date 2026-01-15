// src/hooks/useTriageEmergency.js
import { useMutation } from '@tanstack/react-query';
import { triageEmergency } from '../services/emergencyService';

/**
 * Hook for submitting emergency triage requests.
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

      // Store emergency ID for future requests (status, hospitals, ambulance)
      if (data?.emergencyId) {
        localStorage.setItem('currentEmergencyId', data.emergencyId);
        console.log('📝 Stored Emergency ID:', data.emergencyId);
      }

      return data;
    },
    onError: (error) => {
      console.error('❌ Triage failed:', error.message);
    },
  });
};
