/**
 * GuardianAI SelectedTextAnalyzer Context Menu Module
 * Purpose: Context menu integration adding "Analyse with GuardianAI" to selected text right-click menu:
 *          - Sends ONLY selected text payload to GuardianAI backend
 *          - Stores analysis result in chrome.storage.local for display in popup console.
 */

import { ExtensionScanResult, ExtensionSettings, RiskLevel } from '../shared/types';

const CONTEXT_MENU_ID = 'guardian_ai_analyse_selected_text';
const DEFAULT_BACKEND_URL = 'http://localhost:8000/api/v1';

export class SelectedTextAnalyzer {
  /**
   * Initializes browser right-click context menu for selected text.
   */
  public static initializeContextMenu() {
    chrome.contextMenus.removeAll(() => {
      chrome.contextMenus.create({
        id: CONTEXT_MENU_ID,
        title: '🛡️ Analyse with GuardianAI',
        contexts: ['selection']
      });
    });

    chrome.contextMenus.onClicked.addListener((info, tab) => {
      if (info.menuItemId === CONTEXT_MENU_ID && info.selectionText) {
        this.analyzeSelectedText(info.selectionText, tab);
      }
    });
  }

  /**
   * Analyzes selected text snippet with GuardianAI Backend REST API.
   */
  private static async analyzeSelectedText(selectedText: string, tab?: chrome.tabs.Tab) {
    const cleanText = selectedText.trim().substring(0, 10000);
    console.log('[GuardianAI ContextMenu] Analyzing selected text snippet (length:', cleanText.length, ')');

    try {
      const settingsData = await chrome.storage.sync.get('settings');
      const apiEndpoint = settingsData.settings?.api_endpoint || DEFAULT_BACKEND_URL;

      const response = await fetch(`${apiEndpoint}/analyse/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: cleanText,
          target_persona: 'SENIOR_CITIZENS',
          locale: 'en'
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json = await response.json();
      const resData = json.data;

      const scanResult: ExtensionScanResult = {
        scan_id: resData.scan_id || `scn_txt_${Date.now()}`,
        url: tab?.url || '',
        domain: 'Selected Text Payload',
        risk_level: resData.decision.risk_level as RiskLevel,
        risk_score: resData.decision.final_scam_probability,
        confidence: resData.decision.confidence,
        reasons: resData.decision.reasons || [],
        evidence: resData.decision.evidence || [],
        recommendations: resData.decision.recommendations || [],
        safe_reply: resData.decision.safe_reply,
        scanned_at: Date.now()
      };

      // Store in chrome.storage.local for Extension Popup console
      await chrome.storage.local.set({
        selected_text_scan_result: scanResult,
        last_scanned_text_snippet: cleanText.substring(0, 200)
      });

      // Try to open Extension Popup or trigger Notification
      if (chrome.action && chrome.action.openPopup) {
        chrome.action.openPopup().catch(() => {
          // OpenPopup API fallback
          this.triggerNotification(scanResult);
        });
      } else {
        this.triggerNotification(scanResult);
      }
    } catch (err: any) {
      console.error('[GuardianAI ContextMenu] Failed to analyze selected text:', err);
    }
  }

  private static triggerNotification(result: ExtensionScanResult) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'public/icons/icon-128.png',
      title: `GuardianAI Selected Text Scan: ${result.risk_level}`,
      message: `Scam Score: ${result.risk_score}/100. ${result.reasons[0] || 'Inspection completed.'}`,
      priority: 2
    });
  }
}
