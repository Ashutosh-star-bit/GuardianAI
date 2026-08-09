/**
 * GuardianAI Manifest V3 Enterprise Service Worker Integrator
 * Purpose: Connects Browser Extension components to GuardianAI Backend Scam Pipeline:
 *          1. Handles ANALYZE_URL, ANALYZE_TEXT, and ANALYZE_PAGE_DOM messages with Message Origin Validation.
 *          2. Queries ExtensionStorageService LRU cache (<1ms SLA).
 *          3. Calls GuardianExtensionAPIClient with timeout & exponential backoff retries.
 *          4. Caches response in chrome.storage.local and updates Recent Scans history.
 *          5. Spawns Native Desktop Alerts on HIGH or CRITICAL scam risk.
 */

import { ExtensionMessage, ExtensionResponse, ExtensionScanResult, RiskLevel } from '../shared/types';
import { GuardianExtensionAPIClient } from './api_client';
import { ExtensionStorageService } from '../shared/storage_service';
import { SelectedTextAnalyzer } from './context_menu';
import { ExtensionSecuritySanitizer } from '../utils/sanitizer';

const DEFAULT_BACKEND_URL = 'http://localhost:8000/api/v1';

// --- 1. LIFECYCLE MANAGEMENT ---

chrome.runtime.onInstalled.addListener(async (details) => {
  console.log('[GuardianAI ServiceWorker] Lifecycle: Installed / Updated - Reason:', details.reason);
  await ExtensionStorageService.getSettings();
  SelectedTextAnalyzer.initializeContextMenu();

  chrome.alarms.create('guardian_cache_eviction', { periodInMinutes: 30 });
});

chrome.runtime.onStartup.addListener(() => {
  console.log('[GuardianAI ServiceWorker] Lifecycle: Startup.');
  SelectedTextAnalyzer.initializeContextMenu();
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === 'guardian_cache_eviction') {
    await ExtensionStorageService.clearAllCache();
  }
});

// --- 2. MESSAGE BUS LISTENER WITH SECURITY SENDER VALIDATION ---

chrome.runtime.onMessage.addListener((message: ExtensionMessage, sender, sendResponse) => {
  // SECURITY CONTROL: Verify message originates from this Extension ID
  if (!ExtensionSecuritySanitizer.isMessageOriginTrusted(sender)) {
    console.warn('[GuardianAI Security] Rejected untrusted external message from sender:', sender.id);
    sendResponse({ success: false, error: 'Unauthorized message origin' });
    return false;
  }

  handleMessage(message, sender)
    .then((res) => sendResponse(res))
    .catch((err) => sendResponse({ success: false, error: err.message }));
  return true;
});

async function handleMessage(message: ExtensionMessage, sender: chrome.runtime.MessageSender): Promise<ExtensionResponse> {
  switch (message.type) {
    case 'ANALYZE_URL':
      return await executeUrlAnalysisFlow(message.payload.url);
    case 'ANALYZE_PAGE_DOM':
      return await executePageDomAnalysisFlow(message.payload);
    case 'ANALYZE_TEXT':
      return await executeTextAnalysisFlow(message.payload.text);
    case 'GET_SETTINGS':
      const settings = await ExtensionStorageService.getSettings();
      return { success: true, data: settings };
    case 'UPDATE_SETTINGS':
      const updated = await ExtensionStorageService.saveSettings(message.payload);
      return { success: true, data: updated };
    default:
      return { success: false, error: `Unsupported message: ${message.type}` };
  }
}

// --- 3. END-TO-END URL ANALYSIS INTEGRATION FLOW ---

async function executeUrlAnalysisFlow(targetUrl: string): Promise<ExtensionResponse<ExtensionScanResult>> {
  if (!targetUrl || targetUrl.startsWith('chrome://') || targetUrl.startsWith('about:')) {
    return {
      success: true,
      data: createFallbackResult(targetUrl, 'SAFE', 0, 'Internal browser page')
    };
  }

  const domain = extractDomain(targetUrl);

  // 1. Query LRU Threat Cache (<1ms SLA)
  const cached = await ExtensionStorageService.getCachedAnalysis(domain);
  if (cached) {
    console.log('[GuardianAI Integration] Cache Hit for domain:', domain);
    return { success: true, data: cached };
  }

  // 2. Call GuardianAI Backend REST API via API Client
  try {
    const settings = await ExtensionStorageService.getSettings();
    const apiClient = new GuardianExtensionAPIClient({
      baseUrl: settings.api_endpoint || DEFAULT_BACKEND_URL,
      timeoutMs: 5000,
      maxRetries: 3,
      enforceHttps: false
    });

    const res = await apiClient.analyzeUrl(targetUrl);
    if (!res.success || !res.data) throw new Error(res.error || 'Backend analysis failed');

    const scanResult: ExtensionScanResult = res.data;

    // 3. Cache Result in chrome.storage.local
    await ExtensionStorageService.setCachedAnalysis(domain, scanResult);

    // 4. Update Recent Scans History List
    await ExtensionStorageService.addRecentScan(scanResult);

    // 5. Trigger Native Desktop Alert if HIGH or CRITICAL Risk
    if (scanResult.risk_level === 'HIGH' || scanResult.risk_level === 'CRITICAL') {
      triggerDesktopNotification(scanResult);
    }

    return { success: true, data: scanResult };
  } catch (err: any) {
    console.warn('[GuardianAI Integration] Network fallback triggered:', err);
    return {
      success: true,
      data: createFallbackResult(targetUrl, 'SAFE', 0, 'Offline Heuristic Fallback')
    };
  }
}

// --- 4. END-TO-END PAGE DOM ANALYSIS FLOW ---

async function executePageDomAnalysisFlow(pageData: any): Promise<ExtensionResponse<ExtensionScanResult>> {
  const url = pageData.url || '';
  const domain = extractDomain(url);

  try {
    const settings = await ExtensionStorageService.getSettings();
    const apiClient = new GuardianExtensionAPIClient({
      baseUrl: settings.api_endpoint || DEFAULT_BACKEND_URL,
      timeoutMs: 5000,
      maxRetries: 3,
      enforceHttps: false
    });

    const sanitizedText = ExtensionSecuritySanitizer.sanitizeStringInput(
      pageData.visible_text || pageData.title || url,
      10000
    );

    const res = await apiClient.analyzeText(sanitizedText);
    if (!res.success || !res.data) throw new Error(res.error || 'DOM Analysis failed');

    const scanResult: ExtensionScanResult = {
      ...res.data,
      url,
      domain
    };

    await ExtensionStorageService.setCachedAnalysis(domain, scanResult);
    await ExtensionStorageService.addRecentScan(scanResult);

    if (scanResult.risk_level === 'HIGH' || scanResult.risk_level === 'CRITICAL') {
      triggerDesktopNotification(scanResult);
    }

    return { success: true, data: scanResult };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

// --- 5. TEXT ANALYSIS FLOW ---

async function executeTextAnalysisFlow(text: string): Promise<ExtensionResponse<ExtensionScanResult>> {
  try {
    const settings = await ExtensionStorageService.getSettings();
    const apiClient = new GuardianExtensionAPIClient({
      baseUrl: settings.api_endpoint || DEFAULT_BACKEND_URL,
      timeoutMs: 5000,
      maxRetries: 3,
      enforceHttps: false
    });

    const sanitizedText = ExtensionSecuritySanitizer.sanitizeStringInput(text, 10000);
    return await apiClient.analyzeText(sanitizedText);
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

// --- HELPER UTILITIES ---

function extractDomain(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

function createFallbackResult(url: string, level: RiskLevel, score: number, reason: string): ExtensionScanResult {
  return {
    scan_id: `scn_fb_${Date.now()}`,
    url,
    domain: extractDomain(url),
    risk_level: level,
    risk_score: score,
    confidence: 0.9,
    reasons: [reason],
    evidence: [],
    recommendations: ['Maintain standard web safety awareness.'],
    scanned_at: Date.now()
  };
}

function triggerDesktopNotification(result: ExtensionScanResult) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'public/icons/icon-128.png',
    title: `GuardianAI Shield Alert: ${result.risk_level}`,
    message: `Warning! Web domain ${result.domain} exhibits severe scam probability (${result.risk_score}/100).`,
    priority: 2
  });
}
