/**
 * GuardianAI Browser Extension Shared DTO & Pipeline Type Definitions
 */

export type RiskLevel = 'SAFE' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ThreatEvidenceItem {
  evidence_id: string;
  indicator: string;
  category: string;
  reason: string;
  severity: string;
  confidence: number;
  source: string;
}

export interface UniversalAnalysisRequest {
  url: string;
  text?: string;
  input_type: 'URL' | 'TEXT' | 'DOCUMENT';
  target_persona: 'SENIOR_CITIZENS' | 'GENERAL' | 'STUDENTS';
  locale: string;
  metadata?: Record<string, any>;
}

export interface ExtensionScanResult {
  scan_id: string;
  url: string;
  domain: string;
  risk_level: RiskLevel;
  risk_score: number;
  confidence: number;
  reasons: string[];
  evidence: ThreatEvidenceItem[];
  recommendations: string[];
  safe_reply?: string;
  scanned_at: number;
}

export interface ExtensionSettings {
  senior_mode: boolean;
  auto_block_critical: boolean;
  sound_alerts: boolean;
  highlight_links: boolean;
  api_endpoint: string;
  theme?: 'dark' | 'light' | 'system';
  language?: 'en' | 'hi' | 'hi-en';
  redact_pii?: boolean;
  cache_enabled?: boolean;
}

export type ExtensionMessageType =
  | 'ANALYZE_URL'
  | 'ANALYZE_TEXT'
  | 'ANALYZE_PAGE_DOM'
  | 'GET_DOMAIN_RISK'
  | 'UPDATE_SETTINGS'
  | 'GET_SETTINGS'
  | 'THREAT_DETECTED';

export interface ExtensionMessage<T = any> {
  type: ExtensionMessageType;
  payload: T;
}

export interface ExtensionResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}
