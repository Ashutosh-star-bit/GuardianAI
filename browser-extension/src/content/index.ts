/**
 * GuardianAI Content Script Entry Point
 * Purpose: Executes privacy-preserving DOM content extraction, scans for malicious links & UPI VPAs,
 *          and mounts Shadow DOM threat warning banner when high scam risk is detected.
 */

import { extractStructuredPageContent, StructuredPageContent } from './dom_extractor';
import { scanDomLinksAndForms } from './dom_scanner';
import { mountThreatBannerOverlay } from './overlay_ui';
import { ExtensionResponse, ExtensionScanResult } from '../shared/types';

(function () {
  console.log('[GuardianAI ContentScript] Loaded on page:', window.location.href);

  // 1. Initial Page Security Scan
  runPageSecurityScan();

  // 2. DOM Scanner Execution
  scanDomLinksAndForms();
})();

async function runPageSecurityScan() {
  // 1. Extract Structured Page Content (Visible text, links, forms, title, meta)
  const structuredContent: StructuredPageContent = extractStructuredPageContent();
  console.log(`[GuardianAI ContentScript] DOM extracted in ${structuredContent.extraction_time_ms}ms (Title: "${structuredContent.title}")`);

  try {
    // 2. Transmit structured payload to Service Worker for Threat Analysis
    const res: ExtensionResponse<ExtensionScanResult> = await chrome.runtime.sendMessage({
      type: 'ANALYZE_URL',
      payload: {
        url: window.location.href,
        content: structuredContent
      }
    });

    if (res && res.success && res.data) {
      const scanRes = res.data;

      // 3. Render Shadow DOM Warning Banner if High or Critical Risk
      if (scanRes.risk_level === 'HIGH' || scanRes.risk_level === 'CRITICAL') {
        mountThreatBannerOverlay(scanRes);
      }
    }
  } catch (err) {
    console.warn('[GuardianAI ContentScript] Service worker communication error:', err);
  }
}
