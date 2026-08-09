import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ExtensionSettings } from '../shared/types';
import './options.css';

interface AdvancedSettings extends ExtensionSettings {
  theme: 'dark' | 'light' | 'system';
  language: 'en' | 'hi' | 'hi-en';
  redact_pii: boolean;
  cache_enabled: boolean;
}

export const OptionsApp: React.FC = () => {
  const [settings, setSettings] = useState<AdvancedSettings>({
    senior_mode: true,
    auto_block_critical: true,
    sound_alerts: true,
    highlight_links: true,
    api_endpoint: 'http://localhost:8000/api/v1',
    theme: 'dark',
    language: 'en',
    redact_pii: true,
    cache_enabled: true
  });

  const [savedStatus, setSavedStatus] = useState<string | null>(null);
  const [cacheCount, setCacheCount] = useState<number>(0);

  useEffect(() => {
    // 1. Load settings
    chrome.storage.sync.get('settings', (res) => {
      if (res.settings) {
        setSettings((prev) => ({ ...prev, ...res.settings }));
      }
    });

    // 2. Count cached items in chrome.storage.local
    updateCacheCount();
  }, []);

  const updateCacheCount = async () => {
    const all = await chrome.storage.local.get(null);
    const count = Object.keys(all).filter((k) => k.startsWith('cache_url_')).length;
    setCacheCount(count);
  };

  const handleSave = () => {
    chrome.storage.sync.set({ settings }, () => {
      setSavedStatus('Settings saved successfully! ✅');
      setTimeout(() => setSavedStatus(null), 3000);
    });
  };

  const handleClearCache = async () => {
    const all = await chrome.storage.local.get(null);
    const keysToRemove = Object.keys(all).filter((k) => k.startsWith('cache_url_') || k === 'recent_scans');
    await chrome.storage.local.remove(keysToRemove);
    setCacheCount(0);
    setSavedStatus('LRU Threat Cache cleared successfully! 🧹');
    setTimeout(() => setSavedStatus(null), 3000);
  };

  return (
    <div className="options-container">
      {/* 1. Header & Version Banner */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 800, margin: '0 0 6px 0', color: '#f8fafc' }}>
            🛡️ GuardianAI Extension Console
          </h1>
          <div style={{ fontSize: '13px', color: '#94a3b8' }}>
            Configure real-time web protection, API server endpoints, privacy rules, and language options.
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: '12px', backgroundColor: '#1e293b', padding: '4px 10px', borderRadius: '12px', color: '#a5b4fc', border: '1px solid #334155' }}>
            Version 1.0.0 (Manifest V3)
          </span>
        </div>
      </div>

      {/* 2. Backend REST API Connection Card */}
      <div className="card-section">
        <h3 className="section-title">🌐 Backend API Server Endpoint</h3>
        <div style={{ marginTop: '12px' }}>
          <label className="setting-label" style={{ display: 'block', marginBottom: '6px' }}>
            GuardianAI REST API URL
          </label>
          <input
            type="text"
            className="input-text"
            style={{ width: '100%' }}
            value={settings.api_endpoint}
            onChange={(e) => setSettings({ ...settings, api_endpoint: e.target.value })}
            placeholder="http://localhost:8000/api/v1"
          />
          <div className="setting-desc" style={{ marginTop: '6px' }}>
            Target endpoint for real-time URL and text scam analysis endpoints.
          </div>
        </div>
      </div>

      {/* 3. Theme & Language Customization */}
      <div className="card-section">
        <h3 className="section-title">🎨 Theme & Internationalization</h3>
        <div className="setting-row">
          <div>
            <div className="setting-label">UI Theme Preference</div>
            <div className="setting-desc">Select console aesthetic style for Extension Popup.</div>
          </div>
          <select
            className="select-input"
            value={settings.theme}
            onChange={(e) => setSettings({ ...settings, theme: e.target.value as any })}
          >
            <option value="dark">Dark Mode Cybersecurity (Default)</option>
            <option value="light">Light Mode High-Contrast</option>
            <option value="system">System Default</option>
          </select>
        </div>

        <div className="setting-row">
          <div>
            <div className="setting-label">Target Persona Language</div>
            <div className="setting-desc">Language used for scam explanation reports and safety alerts.</div>
          </div>
          <select
            className="select-input"
            value={settings.language}
            onChange={(e) => setSettings({ ...settings, language: e.target.value as any })}
          >
            <option value="en">English (en)</option>
            <option value="hi">Hindi (hi)</option>
            <option value="hi-en">Hinglish (hi-en)</option>
          </select>
        </div>
      </div>

      {/* 4. Real-Time Protection & Notifications */}
      <div className="card-section">
        <h3 className="section-title">🔔 Notifications & Protection Rules</h3>

        <div className="setting-row">
          <div>
            <div className="setting-label">Senior Citizen Accessibility Mode</div>
            <div className="setting-desc">Enforces high-contrast warning overlays and enlarged fonts.</div>
          </div>
          <input
            type="checkbox"
            checked={settings.senior_mode}
            onChange={(e) => setSettings({ ...settings, senior_mode: e.target.checked })}
          />
        </div>

        <div className="setting-row">
          <div>
            <div className="setting-label">Auto-Block Critical Phishing Sites</div>
            <div className="setting-desc">Prevents page execution when critical scam probability (>80%) is detected.</div>
          </div>
          <input
            type="checkbox"
            checked={settings.auto_block_critical}
            onChange={(e) => setSettings({ ...settings, auto_block_critical: e.target.checked })}
          />
        </div>

        <div className="setting-row">
          <div>
            <div className="setting-label">Desktop Native Threat Alerts</div>
            <div className="setting-desc">Spawns system notifications when high-risk web pages are visited.</div>
          </div>
          <input
            type="checkbox"
            checked={settings.sound_alerts}
            onChange={(e) => setSettings({ ...settings, sound_alerts: e.target.checked })}
          />
        </div>
      </div>

      {/* 5. Privacy & Storage Management */}
      <div className="card-section">
        <h3 className="section-title">🔒 Privacy Controls & Storage Cache</h3>

        <div className="setting-row">
          <div>
            <div className="setting-label">PII Redaction Before Backend Dispatch</div>
            <div className="setting-desc">Automatically strips email addresses and credit card numbers prior to API request.</div>
          </div>
          <input
            type="checkbox"
            checked={settings.redact_pii}
            onChange={(e) => setSettings({ ...settings, redact_pii: e.target.checked })}
          />
        </div>

        <div className="setting-row">
          <div>
            <div className="setting-label">Local Threat LRU Caching</div>
            <div className="setting-desc">Stores up to 2,000 domain risk scores in chrome.storage.local (1-hr TTL).</div>
          </div>
          <input
            type="checkbox"
            checked={settings.cache_enabled}
            onChange={(e) => setSettings({ ...settings, cache_enabled: e.target.checked })}
          />
        </div>

        <div className="setting-row" style={{ paddingTop: '16px' }}>
          <div>
            <div className="setting-label">LRU Cache Storage</div>
            <div className="setting-desc">Currently storing {cacheCount} cached domain threat records.</div>
          </div>
          <button className="btn-danger" onClick={handleClearCache}>
            🧹 Clear Local Cache
          </button>
        </div>
      </div>

      {/* 6. Save Button & Toast */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button className="btn-save" onClick={handleSave}>
          💾 Save All Preferences
        </button>
        {savedStatus && (
          <span style={{ color: '#34d399', fontSize: '14px', fontWeight: 600 }}>
            {savedStatus}
          </span>
        )}
      </div>
    </div>
  );
};

const root = createRoot(document.getElementById('options-root')!);
root.render(<OptionsApp />);
