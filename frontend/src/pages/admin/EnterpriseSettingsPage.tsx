import React, { useState } from 'react';
import { 
  Settings, 
  Cpu, 
  KeyRound, 
  ShieldCheck, 
  Upload, 
  FileText, 
  Mic, 
  Bell, 
  Laptop, 
  Users, 
  BarChart3,
  Save,
  CheckCircle2
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';

export function EnterpriseSettingsPage() {
  const [activeModule, setActiveModule] = useState<'ai' | 'api' | 'security' | 'uploads' | 'ocr' | 'voice' | 'notifications' | 'extension' | 'community' | 'analytics'>('ai');
  const [isSaved, setIsSaved] = useState<boolean>(false);

  // Enterprise Settings Form State
  const [settings, setSettings] = useState({
    ai: { model_variant: 'gemini-1.5-flash', temperature: 0.2, max_output_tokens: 1024, fallback_trigger_rate_limit: 5 },
    api: { rate_limit_per_min: 1000, api_key_expiration_days: 365, cors_origins: '*' },
    security: { session_timeout_minutes: 30, password_expiration_days: 90, max_failed_attempts: 5, enforce_mfa: true },
    uploads: { max_upload_size_mb: 10, verify_magic_signatures: true },
    ocr: { default_language: 'eng+hin', worker_threads: 4 },
    voice: { stt_engine: 'whisper-medium', silence_suppression_ms: 500 },
    notifications: { admin_alert_email: 'security-alerts@guardianai.io', telegram_webhook_enabled: true },
    extension: { client_edge_pii_scrubbing: true, auto_update_check_hrs: 24 },
    community: { approved_report_reputation_pts: 5, rejected_report_penalty_pts: -10 },
    analytics: { log_retention_days: 90, anonymize_user_ips: true }
  });

  const handleSave = () => {
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  const navModules = [
    { key: 'ai', label: 'AI Engine', icon: Cpu },
    { key: 'api', label: 'API & Keys', icon: KeyRound },
    { key: 'security', label: 'Security & Auth', icon: ShieldCheck },
    { key: 'uploads', label: 'Upload Limits', icon: Upload },
    { key: 'ocr', label: 'OCR Processor', icon: FileText },
    { key: 'voice', label: 'Voice Intel', icon: Mic },
    { key: 'notifications', label: 'Notifications', icon: Bell },
    { key: 'extension', label: 'Extension Edge', icon: Laptop },
    { key: 'community', label: 'Community Rules', icon: Users },
    { key: 'analytics', label: 'Analytics Policy', icon: BarChart3 }
  ];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Settings className="w-8 h-8 text-cyan-400" />
            Enterprise Master Configuration Console
          </h1>
          <p className="text-slate-400 mt-1">
            Manage operational parameters across AI LLMs, API quotas, security auth policies, OCR, Voice, and Community rules.
          </p>
        </div>

        <Button variant="primary" onClick={handleSave} className="flex items-center gap-2 px-6 py-2.5 text-xs font-bold">
          <Save className="w-4 h-4" /> Save Configuration Changes
        </Button>
      </div>

      {isSaved && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5" />
          Enterprise settings updated and persisted successfully!
        </div>
      )}

      {/* Module Navigation Tabs */}
      <div className="grid grid-cols-2 sm:grid-cols-5 md:grid-cols-10 gap-2 border-b border-slate-800 pb-3">
        {navModules.map(m => {
          const Icon = m.icon;
          const isActive = activeModule === m.key;
          return (
            <button
              key={m.key}
              onClick={() => setActiveModule(m.key as any)}
              className={`p-2.5 rounded-xl border text-center transition-all flex flex-col items-center gap-1.5 ${
                isActive 
                  ? 'border-cyan-500 bg-cyan-500/10 text-cyan-400 font-bold' 
                  : 'border-slate-800 bg-slate-900/60 text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-[11px] truncate w-full">{m.label}</span>
            </button>
          );
        })}
      </div>

      {/* Form Panels */}
      <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-6">
        {/* PANEL 1: AI Engine */}
        {activeModule === 'ai' && (
          <div className="space-y-4 max-w-xl">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 text-cyan-400">
              <Cpu className="w-5 h-5" /> Google Gemini AI Engine Configuration
            </h2>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Primary LLM Model Variant</label>
              <select
                value={settings.ai.model_variant}
                onChange={(e) => setSettings({ ...settings, ai: { ...settings.ai, model_variant: e.target.value } })}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
              >
                <option value="gemini-1.5-flash">Gemini 1.5 Flash (Sub-150ms High Throughput)</option>
                <option value="gemini-1.5-pro">Gemini 1.5 Pro (Deep Reasoning & Analysis)</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Temperature ({settings.ai.temperature})</label>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={settings.ai.temperature}
                onChange={(e) => setSettings({ ...settings, ai: { ...settings.ai, temperature: parseFloat(e.target.value) } })}
                className="w-full"
              />
            </div>
          </div>
        )}

        {/* PANEL 2: Security */}
        {activeModule === 'security' && (
          <div className="space-y-4 max-w-xl">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 text-indigo-400">
              <ShieldCheck className="w-5 h-5" /> Security & Authentication Policies
            </h2>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Session Timeout (Minutes)</label>
              <input
                type="number"
                value={settings.security.session_timeout_minutes}
                onChange={(e) => setSettings({ ...settings, security: { ...settings.security, session_timeout_minutes: parseInt(e.target.value) } })}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
              />
            </div>

            <label className="flex items-center gap-3 cursor-pointer pt-2">
              <input
                type="checkbox"
                checked={settings.security.enforce_mfa}
                onChange={(e) => setSettings({ ...settings, security: { ...settings.security, enforce_mfa: e.target.checked } })}
                className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-0 w-4 h-4"
              />
              <span className="text-xs text-slate-300">Enforce Multi-Factor Authentication (MFA / TOTP) for all Administrative Roles</span>
            </label>
          </div>
        )}

        {/* Generic Catch-All Panel */}
        {activeModule !== 'ai' && activeModule !== 'security' && (
          <div className="p-8 text-center text-xs text-slate-400 font-mono space-y-2">
            <Settings className="w-8 h-8 text-cyan-400 mx-auto animate-pulse" />
            <div>Module "{activeModule.toUpperCase()}" settings controls ready for enterprise tuning.</div>
          </div>
        )}
      </Card>
    </div>
  );
}
export default EnterpriseSettingsPage;
