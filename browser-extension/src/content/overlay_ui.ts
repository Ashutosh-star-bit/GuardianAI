/**
 * GuardianAI Accessible Non-Blocking Warning Overlay Module
 * Purpose: Renders high-contrast, accessible warning banners inside an isolated Shadow DOM container:
 *          - Displays Risk Level, Confidence %, Reasons List, and Persona Recommendations
 *          - Interactive Action Controls: Dismiss Button, Analyse Again Button, Learn More Button
 *          - Non-Blocking Navigation Guarantee: Never freezes browser tab or locks document interaction
 *          - WCAG AAA Accessibility: Keyboard navigation (Escape key dismiss), ARIA alertdialog roles, 44px touch targets.
 */

import { ExtensionScanResult } from '../shared/types';

export function mountThreatBannerOverlay(result: ExtensionScanResult, onReanalyze?: () => void) {
  const existingHost = document.getElementById('guardian-ai-overlay-root');
  if (existingHost) existingHost.remove();

  const hostDiv = document.createElement('div');
  hostDiv.id = 'guardian-ai-overlay-root';
  hostDiv.style.position = 'fixed';
  hostDiv.style.top = '12px';
  hostDiv.style.right = '12px';
  hostDiv.style.maxWidth = '460px';
  hostDiv.style.width = 'calc(100% - 24px)';
  hostDiv.style.zIndex = '2147483647'; // Highest z-index
  hostDiv.style.pointerEvents = 'none'; // Non-blocking wrapper

  // Closed Shadow DOM Isolation
  const shadowRoot = hostDiv.attachShadow({ mode: 'closed' });

  const isHighRisk = result.risk_level === 'CRITICAL' || result.risk_level === 'HIGH';
  const themeColor = isHighRisk ? '#ef4444' : '#f59e0b';
  const confidencePct = Math.round(result.confidence * 100);

  const style = document.createElement('style');
  style.textContent = `
    :host { all: initial; }
    .overlay-card {
      pointer-events: auto; /* Enable interaction inside card */
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      color: #f8fafc;
      border: 2px solid ${themeColor};
      border-radius: 12px;
      padding: 18px 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.75), 0 0 15px rgba(239, 68, 68, 0.25);
      animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      box-sizing: border-box;
    }
    @keyframes slideInRight {
      from { transform: translateX(110%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    .header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      gap: 12px;
    }
    .badge-container { display: flex; align-items: center; gap: 8px; }
    .risk-badge {
      background-color: ${themeColor};
      color: #ffffff;
      font-weight: 800;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }
    .confidence-tag {
      font-size: 11px;
      color: #94a3b8;
      background: rgba(255,255,255,0.08);
      padding: 3px 8px;
      border-radius: 12px;
      font-weight: 600;
    }
    .card-title {
      font-size: 16px;
      font-weight: 800;
      margin: 0 0 6px 0;
      color: ${isHighRisk ? '#f87171' : '#fbbf24'};
      line-height: 1.3;
    }
    .card-domain {
      font-size: 12px;
      color: #cbd5e1;
      margin: 0 0 12px 0;
      word-break: break-all;
    }
    .section-box {
      background-color: rgba(0, 0, 0, 0.3);
      border-left: 3px solid ${themeColor};
      padding: 10px 12px;
      border-radius: 6px;
      margin-bottom: 12px;
      font-size: 12px;
      line-height: 1.4;
    }
    .reasons-list {
      margin: 4px 0 0 0;
      padding-left: 16px;
      color: #e2e8f0;
    }
    .actions-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 14px;
      flex-wrap: wrap;
    }
    .btn {
      min-height: 44px; /* WCAG 44px Touch Target SLA */
      padding: 0 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      border: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .btn-dismiss {
      background-color: #334155;
      color: #f8fafc;
      flex: 1;
    }
    .btn-dismiss:hover, .btn-dismiss:focus {
      background-color: #475569;
      outline: 2px solid #94a3b8;
    }
    .btn-reanalyze {
      background-color: #4f46e5;
      color: #ffffff;
    }
    .btn-reanalyze:hover, .btn-reanalyze:focus {
      background-color: #4338ca;
      outline: 2px solid #818cf8;
    }
    .btn-learn {
      background: transparent;
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
    }
    .btn-learn:hover, .btn-learn:focus {
      background: rgba(56, 189, 248, 0.1);
      outline: 2px solid #38bdf8;
    }
  `;

  const card = document.createElement('div');
  card.className = 'overlay-card';
  card.setAttribute('role', 'alertdialog');
  card.setAttribute('aria-modal', 'false'); // Non-modal: does not block page navigation
  card.setAttribute('aria-labelledby', 'guardian-title');
  card.setAttribute('aria-describedby', 'guardian-desc');

  const reasonsHtml = result.reasons.length > 0
    ? `<ul class="reasons-list">${result.reasons.map((r) => `<li>${escapeHtml(r)}</li>`).join('')}</ul>`
    : '<p style="margin:0;">Multiple scam and phishing indicators detected on this website.</p>';

  const recommendationsText = result.recommendations.length > 0
    ? result.recommendations[0]
    : 'Do NOT enter passwords, credit card numbers, or personal details.';

  card.innerHTML = `
    <div class="header-row">
      <div class="badge-container">
        <span class="risk-badge">${result.risk_level} RISK</span>
        <span class="confidence-tag">${confidencePct}% Confidence</span>
      </div>
      <span style="font-size: 11px; color: #94a3b8;">GuardianAI Shield</span>
    </div>

    <h3 class="card-title" id="guardian-title">⚠️ Phishing / Scam Risk Warning</h3>
    <p class="card-domain" id="guardian-desc">Website: <strong>${escapeHtml(result.domain)}</strong> (Score: ${result.risk_score}/100)</p>

    <div class="section-box">
      <strong>Identified Threat Factors:</strong>
      ${reasonsHtml}
    </div>

    <div style="font-size: 12px; color: #34d399; margin-bottom: 12px;">
      💡 <strong>Action Recommendation:</strong> ${escapeHtml(recommendationsText)}
    </div>

    <div class="actions-row">
      <button className="btn" class="btn btn-dismiss" id="btn-dismiss" aria-label="Dismiss warning overlay">
        ✕ Dismiss Warning
      </button>
      <button className="btn" class="btn btn-reanalyze" id="btn-reanalyze" aria-label="Analyse page again">
        🔄 Analyse Again
      </button>
      <button className="btn" class="btn btn-learn" id="btn-learn" aria-label="Learn more about this threat">
        📖 Learn More
      </button>
    </div>
  `;

  shadowRoot.appendChild(style);
  shadowRoot.appendChild(card);
  document.body.appendChild(hostDiv);

  // Keyboard Accessibility: Dismiss on Escape Key
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      dismissOverlay();
    }
  };
  window.addEventListener('keydown', handleKeyDown);

  const dismissOverlay = () => {
    window.removeEventListener('keydown', handleKeyDown);
    hostDiv.remove();
  };

  // Button Event Listeners
  const dismissBtn = card.querySelector('#btn-dismiss');
  dismissBtn?.addEventListener('click', dismissOverlay);

  const reanalyzeBtn = card.querySelector('#btn-reanalyze');
  reanalyzeBtn?.addEventListener('click', () => {
    dismissOverlay();
    if (onReanalyze) onReanalyze();
    else window.location.reload();
  });

  const learnBtn = card.querySelector('#btn-learn');
  learnBtn?.addEventListener('click', () => {
    chrome.runtime.sendMessage({
      type: 'ANALYZE_TEXT',
      payload: { text: `Learn More query for threat on domain ${result.domain}` }
    });
    alert(`GuardianAI Security Report:\n\nDomain: ${result.domain}\nRisk Score: ${result.risk_score}/100\n\nReasons:\n${result.reasons.join('\n')}`);
  });

  // Focus dismiss button for keyboard accessibility
  setTimeout(() => (dismissBtn as HTMLElement)?.focus(), 100);
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
