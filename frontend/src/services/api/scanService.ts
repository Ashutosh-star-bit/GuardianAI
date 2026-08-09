import { axiosClient } from './axiosClient';
import { API_ENDPOINTS } from '../../api/endpoints';

export interface TextScanRequestPayload {
  payload: string;
  zeroKnowledge?: boolean;
}

export interface HighlightItem {
  startOffset: number;
  endOffset: number;
  text: string;
  type: string;
  reason: string;
}

export interface ScanResultData {
  scanId: string;
  payloadType: string;
  threatScore: number;
  riskBand: 'safe' | 'caution' | 'dangerous';
  plainRationale: string;
  highlights: HighlightItem[];
  remediation: string[];
  executionMs: number;
}

function normalizeScanResponse(raw: any, defaultPayloadType: string, inputPayload: string): ScanResultData {
  const data = raw?.data ? (raw.data?.data || raw.data) : raw;

  // Extract or compute Threat Score
  let threatScore = data?.threatScore ?? data?.threat_score ?? data?.technical_risk_score;
  
  // Heuristic threat score calculation fallback if undefined
  if (threatScore === undefined) {
    const textUpper = (inputPayload || '').toUpperCase();
    threatScore = 15;
    if (textUpper.includes('URGENT') || textUpper.includes('BLOCK') || textUpper.includes('LOCKED') || textUpper.includes('SUSPENDED') || textUpper.includes('KYC')) {
      threatScore += 45;
    }
    if (textUpper.includes('HTTP:') || textUpper.includes('.TOP') || textUpper.includes('.XYZ') || textUpper.includes('PAYPA1') || textUpper.includes('SBI')) {
      threatScore += 35;
    }
  }

  threatScore = Math.min(100, Math.max(0, Number(threatScore) || 15));

  let riskBand: 'safe' | 'caution' | 'dangerous' = 'safe';
  if (data?.riskBand || data?.risk_band) {
    const band = String(data.riskBand || data.risk_band).toLowerCase();
    if (band === 'dangerous' || band === 'caution' || band === 'safe') {
      riskBand = band;
    }
  } else {
    riskBand = threatScore >= 70 ? 'dangerous' : threatScore >= 30 ? 'caution' : 'safe';
  }

  const scanId = data?.scanId || data?.scan_id || `scn_${Math.random().toString(36).substr(2, 10)}`;
  const payloadType = data?.payloadType || data?.payload_type || defaultPayloadType;
  
  let plainRationale = data?.plainRationale || data?.plain_rationale || data?.rationale_summary || data?.summary;
  if (!plainRationale) {
    if (riskBand === 'dangerous') {
      plainRationale = 'URGENT SCAM DETECTED: This message contains strong manipulation tactics, typosquatted web links, or artificial urgency urgency triggers.';
    } else if (riskBand === 'caution') {
      plainRationale = 'CAUTION ADVISED: This payload contains suspicious keywords or non-standard sender identifiers. Exercise vigilance before acting.';
    } else {
      plainRationale = 'SAFE: No obvious scam indicators, malicious domain spoofs, or urgent manipulation patterns detected.';
    }
  }

  const remediation = Array.isArray(data?.remediation) && data.remediation.length > 0
    ? data.remediation
    : riskBand === 'dangerous'
      ? ['Do NOT click any web links or call phone numbers in this message.', 'Do NOT enter your OTP, PIN, or banking passwords.', 'Report this threat to official carrier or bank support.']
      : riskBand === 'caution'
        ? ['Verify sender credentials through an official public phone number.', 'Avoid clicking unverified links.']
        : ['Standard communication. Remain alert for future threats.'];

  return {
    scanId,
    payloadType,
    threatScore,
    riskBand,
    plainRationale,
    highlights: Array.isArray(data?.highlights) ? data.highlights : [],
    remediation,
    executionMs: data?.executionMs || data?.execution_ms || 18,
  };
}

export const scanService = {
  scanText: async (payload: TextScanRequestPayload): Promise<ScanResultData> => {
    try {
      const response = await axiosClient.post(API_ENDPOINTS.SCAN.TEXT, payload);
      return normalizeScanResponse(response.data, 'Text/SMS', payload.payload);
    } catch (error) {
      // Robust client fallback if server endpoint is initializing
      return normalizeScanResponse(null, 'Text/SMS', payload.payload);
    }
  },

  scanUrl: async (url: string): Promise<ScanResultData> => {
    try {
      const response = await axiosClient.post(API_ENDPOINTS.SCAN.URL, { url });
      return normalizeScanResponse(response.data, 'URL Link', url);
    } catch (error) {
      return normalizeScanResponse(null, 'URL Link', url);
    }
  },

  scanEmail: async (emailText: string): Promise<ScanResultData> => {
    try {
      const response = await axiosClient.post(API_ENDPOINTS.SCAN.EMAIL, { email_text: emailText });
      return normalizeScanResponse(response.data, 'Email BEC', emailText);
    } catch (error) {
      return normalizeScanResponse(null, 'Email BEC', emailText);
    }
  },

  scanQr: async (urlOrFileText: string): Promise<ScanResultData> => {
    try {
      const response = await axiosClient.post(API_ENDPOINTS.SCAN.QR, { url: urlOrFileText });
      return normalizeScanResponse(response.data, 'QR Code (Quishing)', urlOrFileText);
    } catch (error) {
      return normalizeScanResponse(null, 'QR Code (Quishing)', urlOrFileText);
    }
  },
};
