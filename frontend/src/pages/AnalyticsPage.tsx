import React from 'react';
import {
  BarChart3,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  Zap,
  Activity,
  ArrowUpRight,
  TrendingUp,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { Card } from '../components/common/Card';
import { useAuth } from '../context/AuthContext';

export const AnalyticsPage: React.FC = () => {
  const { scanHistory, currentUser } = useAuth();

  const totalScans = scanHistory.length;
  const dangerousCount = scanHistory.filter((s) => s.riskBand === 'dangerous').length;
  const cautionCount = scanHistory.filter((s) => s.riskBand === 'caution').length;
  const safeCount = scanHistory.filter((s) => s.riskBand === 'safe').length;

  const avgThreatScore =
    totalScans > 0
      ? Math.round(scanHistory.reduce((acc, s) => acc + s.threatScore, 0) / totalScans)
      : 0;

  // Breakdown by channel
  const messageScans = scanHistory.filter((s) => s.payloadType.toLowerCase().includes('text') || s.payloadType.toLowerCase().includes('sms')).length;
  const emailScans = scanHistory.filter((s) => s.payloadType.toLowerCase().includes('email')).length;
  const urlScans = scanHistory.filter((s) => s.payloadType.toLowerCase().includes('url')).length;
  const qrScans = scanHistory.filter((s) => s.payloadType.toLowerCase().includes('qr')).length;

  return (
    <PageTransition className="space-y-6 py-4">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <BarChart3 className="w-4 h-4" />
          <span>Real-Time Threat Telemetry</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Threat Analytics Dashboard</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Calculated dynamically from your active scan history records and AI detection pipeline telemetry.
        </p>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 border-slate-800 bg-slate-900/90 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Total AI Scans</span>
            <Activity className="w-4 h-4 text-sky-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">{totalScans}</div>
          <p className="text-[10px] text-slate-500">Live session inspections</p>
        </Card>

        <Card className="p-4 border-red-500/30 bg-red-950/10 space-y-2">
          <div className="flex items-center justify-between text-xs text-red-300">
            <span>High Risk Threats</span>
            <ShieldAlert className="w-4 h-4 text-red-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-red-400 font-mono">{dangerousCount}</div>
          <p className="text-[10px] text-red-300/70">Neutralized scams</p>
        </Card>

        <Card className="p-4 border-amber-500/30 bg-amber-950/10 space-y-2">
          <div className="flex items-center justify-between text-xs text-amber-300">
            <span>Caution Warnings</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-amber-400 font-mono">{cautionCount}</div>
          <p className="text-[10px] text-amber-300/70">Suspicious payloads</p>
        </Card>

        <Card className="p-4 border-emerald-500/30 bg-emerald-950/10 space-y-2">
          <div className="flex items-center justify-between text-xs text-emerald-300">
            <span>Average Risk Score</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">{avgThreatScore}/100</div>
          <p className="text-[10px] text-emerald-300/70">Composite risk index</p>
        </Card>
      </div>

      {/* Channel Breakdown */}
      <Card className="p-6 border-slate-800 bg-slate-900/90 space-y-4">
        <h2 className="text-lg font-black text-white flex items-center gap-2">
          <Zap className="w-5 h-5 text-sky-400" />
          <span>Threat Vectors Breakdown</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-1">
            <span className="text-xs text-slate-400 block font-bold">SMS / Message Scans</span>
            <span className="text-xl font-black text-white font-mono">{messageScans}</span>
          </div>

          <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-1">
            <span className="text-xs text-slate-400 block font-bold">Email BEC Scans</span>
            <span className="text-xl font-black text-white font-mono">{emailScans}</span>
          </div>

          <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-1">
            <span className="text-xs text-slate-400 block font-bold">URL / Web Link Scans</span>
            <span className="text-xl font-black text-white font-mono">{urlScans}</span>
          </div>

          <div className="bg-slate-950 border border-slate-800 p-4 rounded-2xl space-y-1">
            <span className="text-xs text-slate-400 block font-bold">QR Quishing Scans</span>
            <span className="text-xl font-black text-white font-mono">{qrScans}</span>
          </div>
        </div>
      </Card>
    </PageTransition>
  );
};
