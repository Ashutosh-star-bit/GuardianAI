import { useMutation, useQueryClient } from '@tanstack/react-query';
import { scanService, TextScanRequestPayload, ScanResultData } from '../services/api/scanService';
import { useToast } from '../context/ToastContext';
import { NormalizedApiError } from '../services/api/axiosClient';

/**
 * GuardianAI Scan Mutation Custom Hook
 * Purpose: Provides a typed React Query mutation for submitting scan payloads with automatic toast notification feedback.
 */
export const useScanMutation = () => {
  const queryClient = useQueryClient();
  const { showToast } = useToast();

  return useMutation<ScanResultData, NormalizedApiError, TextScanRequestPayload>({
    mutationFn: (payload) => scanService.scanText(payload),
    onSuccess: (data) => {
      showToast('success', 'Scan Completed', `Risk Band: ${data.riskBand.toUpperCase()} (${data.threatScore}/100)`);
      queryClient.invalidateQueries({ queryKey: ['scans', 'history'] });
    },
    onError: (error) => {
      showToast('error', 'Scan Execution Failed', error.message || 'An error occurred during analysis.');
    },
  });
};
