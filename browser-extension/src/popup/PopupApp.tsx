import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ExtensionScanResult, ExtensionSettings } from '../shared/types';
import './popup.css';

export const PopupApp: React.FC = () => {
  const [currentUrl, setCurrentUrl] = useState<string>('');
  const [currentDomain, setCurrentDomain] = useState<string>('');
  const [scanResult, setScanResult] = useState<ExtensionScanResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [recentScans, setRecentScans] = useState<ExtensionScanResult[]>([]);
  const [settings, setSettings] = useState<ExtensionSettings>({
    senior_mode: true,
    auto_block_critical: true,
    sound_alerts: true,
    highlight_links: true,
    api_endpoint: 'http://localhost:8000/api/v1'
  });

  useEffect(() => {
    // 1. Fetch current tab details
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]?.url) {
        const url = tabs[0].url;
        setCurrentUrl(url);
        try {
          const parsed = new URL(url);
          setCurrentDomain(parsed.hostname);
        } catch {
          setCurrentDomain(url);
        }
        analyzeTabUrl(url);
      } else {
        setLoading(false);
      }
    });

    // 2. Load settings and recent scans history
    chrome.storage.sync.get('settings', (res) => {
      if (res.settings) setSettings(res.settings);
    });

    loadRecentScansHistory();
  }, []);

  const analyzeTabUrl = async (url: string) => {
    setLoading(true);
    chrome.runtime.sendMessage({ type: 'ANALYZE_URL', payload: { url } }, (res) => {
      setLoading(false);
      if (res && res.success && res.data) {
        setScanResult(res.data);
        saveToRecentHistory(res.data);
      }
    });
  };

  const loadRecentScansHistory = async () => {
    const data = await chrome.storage.local.get('recent_scans');
    if (data.recent_scans) {
      setRecentScans(data.recent_scans);
    }
  };

  const saveToRecentHistory = async (newResult: ExtensionScanResult) => {
    const existing = await chrome.storage.local.get('recent_scans');
    let list: ExtensionScanResult[] = existing.recent_scans || [];
    list = [newResult, ...list.filter((r) => r.domain !== newResult.domain)].slice(0, 5);
    await chrome.storage.local.set({ recent_scans: list });
    setRecentScans(list);
  };

  const getRiskBadgeClass = (level: string) => {
    if (level === 'CRITICAL' || level === 'HIGH') return 'risk-badge badge-critical';
    if (level === 'MEDIUM' || level === 'LOW') return 'risk-badge badge-medium';
    return 'risk-badge badge-safe';
  };

  return (
    <div className="popup-container">
      {/* 1. Header Bar */}
      <div className="header-bar">
        <div className="brand-logo">
          <div className="shield-pulse"></div>
          <span style={{ fontWeight: 800, fontSize: '15px', color: '#f8fafc' }}>GuardianAI Protection</span>
        </div>
        <span style={{ fontSize: '11px', backgroundColor: 'rgba(255,255,255,0.08)', padding: '3px 8px', borderRadius: '12px', color: '#94a3b8' }}>
          v1.0.0
        </span>
      </div>

      {/* 2. Active Tab Website URL & Domain Card */}
      <div className="glass-card">
        <div style={{ fontSize: '11px', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600, marginBottom: '4px' }}>
          Active Web Domain
        </div>
        <div style={{ fontSize: '15px', fontWeight: 700, color: '#f8fafc', wordBreak: 'break-all', marginBottom: '4px' }}>
          {currentDomain || 'Unknown Domain'}
        </div>
        <div style={{ fontSize: '11px', color: '#64748b', wordBreak: 'break-all', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {currentUrl || 'No active tab'}
        </div>
      </div>

      {/* 3. Loading Animation vs Quick Risk Status Card */}
      {loading ? (
        <div className="glass-card radar-spinner-container">
          <div className="radar-spinner"></div>
          <div style={{ fontSize: '13px', color: '#cbd5e1', fontWeight: 500 }}>
            Inspecting URL Threat Landscape...
          </div>
        </div>
      ) : scanResult ? (
        <div className="glass-card" style={{ borderLeft: `4px solid ${scanResult.risk_score > 50 ? '#ef4444' : '#10b981'}` }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '12px', color: '#94a3b8', fontWeight: 600 }}>Quick Risk Status</span>
            <span className={getRiskBadgeClass(scanResult.risk_level)}>{scanResult.risk_level}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '8px' }}>
            <span style={{ fontSize: '28px', fontWeight: 800, color: scanResult.risk_score > 50 ? '#f87171' : '#34d399' }}>
              {scanResult.risk_score}
            </span>
            <span style={{ fontSize: '13px', color: '#64748b' }}>/ 100 Scam Risk Probability</span>
          </div>

          {scanResult.reasons.length > 0 && (
            <div style={{ fontSize: '12px', color: '#cbd5e1', backgroundColor: 'rgba(0,0,0,0.25)', padding: '8px 10px', borderRadius: '6px', marginTop: '8px' }}>
              ⚠️ {scanResult.reasons[0]}
            </div>
          )}
        </div>
      ) : null}

      {/* 4. Manual Scan Button */}
      <button
        className="btn-primary"
        disabled={loading || !currentUrl}
        onClick={() => analyzeTabUrl(currentUrl)}
      >
        🔍 Rescan Active Page Now
      </button>

      {/* 5. Recent Scans List */}
      {recentScans.length > 0 && (
        <div className="glass-card" style={{ padding: '12px 14px' }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: '#e2e8f0', marginBottom: '10px' }}>
            Recent Scanned Domains
          </div>
          <div className="recent-list">
            {recentScans.map((scan, idx) => (
              <div key={idx} className="recent-item">
                <div>
                  <div style={{ fontSize: '12px', fontWeight: 600, color: '#f1f5f9' }}>{scan.domain}</div>
                  <div style={{ fontSize: '10px', color: '#64748b' }}>
                    {new Date(scan.scanned_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                <span className={getRiskBadgeClass(scan.risk_level)} style={{ fontSize: '10px', padding: '2px 6px' }}>
                  {scan.risk_level}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 6. Settings Shortcut Footer */}
      <div style={{ marginTop: 'auto', textAlign: 'center', paddingTop: '8px' }}>
        <button
          onClick={() => chrome.runtime.openOptionsPage()}
          style={{
            background: 'none',
            border: 'none',
            color: '#818cf8',
            fontSize: '12px',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px'
          }}
        >
          ⚙️ Extension Settings & Preferences
        </button>
      </div>
    </div>
  );
};

const root = createRoot(document.getElementById('popup-root')!);
root.render(<PopupApp />);
