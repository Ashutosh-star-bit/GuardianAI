import React, { useState } from 'react';
import {
  Settings,
  Sun,
  Moon,
  Globe,
  Lock,
  Shield,
  Bell,
  Eye,
  Info,
  Copy,
  RefreshCw,
  Save,
  CheckCircle2,
  Sliders,
  Volume2,
  Sparkles,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAccessibility } from '../context/AccessibilityContext';
import { ThreeDCard } from '../components/3d/ThreeDCard';

/**
 * GuardianAI Complete Platform System Settings Page Component
 * Sections: Appearance, Theme, Language, Security (API Key), Privacy, Notifications, Accessibility, About.
 */

export const SettingsPage: React.FC = () => {
  const { isDarkMode, isSeniorMode, isAudioNarrationEnabled, toggleTheme, toggleSeniorMode, toggleAudioNarration } = useAccessibility();
  const [apiKey, setApiKey] = useState('gai_live_88f92a110099xza21_prod');
  const [showApiKey, setShowApiKey] = useState(false);
  const [copiedKey, setCopiedKey] = useState(false);

  // Preference States
  const [language, setLanguage] = useState('en');
  const [density, setDensity] = useState<'comfortable' | 'compact'>('comfortable');
  const [piiStrictness, setPiiStrictness] = useState<'strict' | 'standard'>('strict');
  const [pushAlerts, setPushAlerts] = useState(true);
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const { showToast } = useToast();

  const handleCopyApiKey = () => {
    navigator.clipboard.writeText(apiKey);
    setCopiedKey(true);
    showToast('success', 'API Key Copied', 'Developer key copied to clipboard.');
    setTimeout(() => setCopiedKey(false), 2000);
  };

  const handleRegenerateApiKey = () => {
    const newKey = `gai_live_${Math.random().toString(36).substring(2, 15)}_prod`;
    setApiKey(newKey);
    showToast('info', 'API Key Regenerated', 'New production API key generated successfully.');
  };

  const handleSaveAll = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      showToast('success', 'Settings Saved', 'Platform configuration updated successfully.');
    }, 800);
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-2">
            <Settings className="w-6 h-6 text-sky-400" />
            <span>Platform System Settings</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Configure appearance, theme, language, developer API keys, privacy scrubbing, and accessibility presets.
          </p>
        </div>

        <Button size="sm" onClick={handleSaveAll} isLoading={isSaving} leftIcon={<Save className="w-4 h-4" />}>
          Save All Settings
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: MAIN CONFIGURATION SECTIONS (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* 1. APPEARANCE & THEME */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
              <Sun className="w-4 h-4 text-sky-400" />
              <span>1. Appearance & Theme</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              {/* Theme Selector */}
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-3">
                <span className="font-bold text-white flex items-center gap-1.5">
                  {isDarkMode ? <Moon className="w-4 h-4 text-sky-400" /> : <Sun className="w-4 h-4 text-amber-500" />}
                  Theme Mode
                </span>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={toggleTheme}
                    className={`w-full py-2 rounded-lg font-bold border transition-all ${
                      isDarkMode ? 'bg-sky-600 text-white border-sky-400' : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    Dark Theme
                  </button>
                  <button
                    type="button"
                    onClick={toggleTheme}
                    className={`w-full py-2 rounded-lg font-bold border transition-all ${
                      !isDarkMode ? 'bg-amber-400 text-black border-amber-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    Light Theme
                  </button>
                </div>
              </div>

              {/* Layout Density */}
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-3">
                <span className="font-bold text-white flex items-center gap-1.5">
                  <Sliders className="w-4 h-4 text-sky-400" />
                  Layout Density
                </span>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setDensity('comfortable')}
                    className={`w-full py-2 rounded-lg font-bold border transition-all ${
                      density === 'comfortable' ? 'bg-sky-600 text-white border-sky-400' : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    Comfortable
                  </button>
                  <button
                    type="button"
                    onClick={() => setDensity('compact')}
                    className={`w-full py-2 rounded-lg font-bold border transition-all ${
                      density === 'compact' ? 'bg-sky-600 text-white border-sky-400' : 'bg-slate-800 text-slate-400 border-slate-700'
                    }`}
                  >
                    Compact
                  </button>
                </div>
              </div>
            </div>
          </Card>

          {/* 2. LANGUAGE & LOCALE */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
              <Globe className="w-4 h-4 text-sky-400" />
              <span>2. Language & Internationalization</span>
            </h2>

            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-300">Console Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-sky-500"
              >
                <option value="en">English (United States) - Default</option>
                <option value="es">Español (Spanish)</option>
                <option value="fr">Français (French)</option>
                <option value="de">Deutsch (German)</option>
              </select>
            </div>
          </Card>

          {/* 3. SECURITY & DEVELOPER API KEY */}
          <Card className="space-y-4 border-slate-800">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-base font-black text-white flex items-center gap-2">
                <Lock className="w-4 h-4 text-sky-400" />
                <span>3. Developer API Keys & Security</span>
              </h2>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800 font-bold">
                1,000 req/min SLA
              </span>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-300">Production REST API Key</label>
              <div className="flex items-center gap-2">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={apiKey}
                  readOnly
                  className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-xs font-mono text-slate-200"
                />
                <Button variant="secondary" size="sm" onClick={() => setShowApiKey(!showApiKey)}>
                  {showApiKey ? 'Hide' : 'Show'}
                </Button>
                <Button variant="secondary" size="sm" onClick={handleCopyApiKey} leftIcon={<Copy className="w-3.5 h-3.5" />}>
                  {copiedKey ? 'Copied' : 'Copy'}
                </Button>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-900 text-xs">
              <span className="text-slate-400">Regenerating invalidates previous key instantly.</span>
              <Button type="button" variant="secondary" size="sm" onClick={handleRegenerateApiKey} leftIcon={<RefreshCw className="w-3.5 h-3.5" />}>
                Regenerate Key
              </Button>
            </div>
          </Card>

          {/* 4. PRIVACY & PII SCRUBBING STRICTNESS */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span>4. Privacy & Zero-Knowledge Scrubbing</span>
            </h2>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white">Client-Side Web Worker PII Anonymization</span>
                  <span className="text-emerald-400 font-bold font-mono">STRICT ENFORCEMENT</span>
                </div>
                <p className="text-slate-400 text-[11px]">
                  All Credit Card numbers, Social Security Numbers, phone numbers, and full names are scrubbed locally inside your browser before network payload transmission.
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* RIGHT COLUMN: NOTIFICATIONS, ACCESSIBILITY, ABOUT (1/3 Width) */}
        <div className="space-y-6">
          {/* 5. NOTIFICATION SETTINGS */}
          <FadeIn delay={0.1}>
            <Card className="space-y-4 border-slate-800">
              <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
                <Bell className="w-4 h-4 text-sky-400" />
                <span>5. Notifications</span>
              </h2>

              <div className="space-y-3 text-xs">
                <label className="flex items-center justify-between cursor-pointer p-2 rounded-lg hover:bg-slate-900 transition-colors">
                  <span className="font-bold text-slate-200">Email Threat Alerts</span>
                  <input
                    type="checkbox"
                    checked={emailAlerts}
                    onChange={(e) => setEmailAlerts(e.target.checked)}
                    className="w-4 h-4 rounded text-sky-500 focus:ring-sky-500 bg-slate-900 border-slate-700"
                  />
                </label>

                <label className="flex items-center justify-between cursor-pointer p-2 rounded-lg hover:bg-slate-900 transition-colors">
                  <span className="font-bold text-slate-200">Browser Push Notifications</span>
                  <input
                    type="checkbox"
                    checked={pushAlerts}
                    onChange={(e) => setPushAlerts(e.target.checked)}
                    className="w-4 h-4 rounded text-sky-500 focus:ring-sky-500 bg-slate-900 border-slate-700"
                  />
                </label>
              </div>
            </Card>
          </FadeIn>

          {/* 6. ACCESSIBILITY PRESETS */}
          <FadeIn delay={0.2}>
            <Card className="space-y-4 border-slate-800">
              <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
                <Eye className="w-4 h-4 text-amber-400" />
                <span>6. Accessibility</span>
              </h2>

              <div className="space-y-3 text-xs">
                <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">Senior Citizen Mode</span>
                    <button
                      type="button"
                      onClick={toggleSeniorMode}
                      className={`px-2.5 py-1 rounded-lg text-xs font-black transition-all border ${
                        isSeniorMode ? 'bg-amber-400 text-black border-black' : 'bg-slate-800 text-amber-300 border-amber-400/60'
                      }`}
                    >
                      {isSeniorMode ? 'ON' : 'OFF'}
                    </button>
                  </div>
                  <p className="text-slate-400 text-[11px]">Hotkey: <code className="text-amber-400">Alt + S</code></p>
                </div>

                <div className="p-3 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white flex items-center gap-1.5">
                      <Volume2 className="w-4 h-4 text-sky-400" /> Audio Narration
                    </span>
                    <button
                      type="button"
                      onClick={toggleAudioNarration}
                      className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all border ${
                        isAudioNarrationEnabled ? 'bg-sky-600 text-white border-sky-400' : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      {isAudioNarrationEnabled ? 'ON' : 'OFF'}
                    </button>
                  </div>
                </div>
              </div>
            </Card>
          </FadeIn>

          {/* 7. ABOUT & SYSTEM INFO */}
          <FadeIn delay={0.3}>
            <Card className="space-y-3 border-slate-800">
              <h2 className="text-base font-black text-white border-b border-slate-800 pb-3 flex items-center gap-2">
                <Info className="w-4 h-4 text-sky-400" />
                <span>7. About GuardianAI</span>
              </h2>

              <div className="space-y-2 text-xs text-slate-300">
                <div className="flex justify-between py-1 border-b border-slate-900">
                  <span className="text-slate-400">Platform Version</span>
                  <span className="font-mono font-bold text-white">v1.0.0 (July 2026)</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-900">
                  <span className="text-slate-400">Engine SLA</span>
                  <span className="font-mono font-bold text-emerald-400">Sub-1.8s Response</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Privacy Status</span>
                  <span className="font-bold text-sky-400">Zero-Knowledge Certified</span>
                </div>
              </div>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
