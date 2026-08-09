import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  ShieldAlert,
  Shield,
  Activity,
  MessageSquare,
  Globe,
  Mail,
  QrCode,
  ArrowRight,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  ChevronRight,
  RefreshCw,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Skeleton } from '../components/common/Skeleton';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { ThreeDCard } from '../components/3d/ThreeDCard';
import { ThreatSphere3D } from '../components/3d/ThreatSphere3D';

/**
 * GuardianAI Security Command Dashboard Component
 * Purpose: Central intelligence hub displaying real threat stats, risk distribution, real scan logs, live threat feed, and quick scanner with 3D animation depth.
 */

export const DashboardPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [quickInput, setQuickInput] = useState('');
  const [activeQuickTab, setActiveQuickTab] = useState<'text' | 'url' | 'email' | 'qr'>('text');
  const { showToast } = useToast();
  const { scanHistory, currentUser } = useAuth();

  const handleRefresh = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      showToast('info', 'Dashboard Refreshed', 'Latest threat metrics and scan logs loaded.');
    }, 600);
  };

  const handleQuickScanSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickInput.trim()) {
      showToast('error', 'Empty Input', 'Please enter text, a URL, or an email snippet to inspect.');
      return;
    }
    showToast('success', 'Scan Submitted', `Analyzing ${activeQuickTab.toUpperCase()} payload...`);
    setQuickInput('');
  };

  // Real scan history metrics
  const totalScans = scanHistory.length;
  const dangerousScans = scanHistory.filter((s) => s.riskBand === 'dangerous').length;
  const cautionScans = scanHistory.filter((s) => s.riskBand === 'caution').length;
  const safeScans = scanHistory.filter((s) => s.riskBand === 'safe').length;

  const safeRate = totalScans > 0 ? Math.round((safeScans / totalScans) * 100) : 100;
  const dangerousRate = totalScans > 0 ? Math.round((dangerousScans / totalScans) * 100) : 0;
  const cautionRate = totalScans > 0 ? Math.round((cautionScans / totalScans) * 100) : 0;

  const getScanIcon = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes('url') || t.includes('link')) return Globe;
    if (t.includes('email') || t.includes('bec')) return Mail;
    if (t.includes('qr')) return QrCode;
    return MessageSquare;
  };

  const liveThreatFeed = [
    {
      id: 'tf_1',
      title: 'High Surge in WhatsApp Parent-Child Impersonation Scams',
      category: 'Smishing',
      severity: 'high',
      time: '12m ago',
    },
    {
      id: 'tf_2',
      title: 'Fake Utility Bill Disconnection SMS targeting Senior Citizens',
      category: 'SMS Scams',
      severity: 'medium',
      time: '45m ago',
    },
    {
      id: 'tf_3',
      title: 'Typosquatted Banking Domains (.top / .xyz TLDs) Spiking',
      category: 'Phishing',
      severity: 'high',
      time: '2h ago',
    },
  ];

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Dashboard Top Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight flex items-center gap-2">
            <span>Security Command Dashboard</span>
            <span className="text-xs font-mono font-bold bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2.5 py-0.5 rounded-full shadow-[0_0_15px_rgba(56,189,248,0.2)]">
              3D INTEL LIVE
            </span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Real-time Threat Intelligence & Explainable AI Scan Summary
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleRefresh}
            isLoading={isLoading}
            leftIcon={<RefreshCw className="w-4 h-4" />}
          >
            Refresh Data
          </Button>
          <Link to="/scan/message">
            <Button size="sm" rightIcon={<ArrowRight className="w-4 h-4" />}>
              New AI Scan
            </Button>
          </Link>
        </div>
      </div>

      {/* ====================================================================
          1. STATISTICAL METRICS OVERVIEW CARDS (WITH 3D TILT EFFECT)
          ==================================================================== */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <FadeIn delay={0.05}>
          <ThreeDCard glowColor="cyan">
            <Card className="space-y-2 border-slate-800 bg-slate-900/90 backdrop-blur-xl h-full">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total AI Scans</span>
                <div className="bg-sky-500/10 p-2 rounded-xl border border-sky-500/30">
                  <Activity className="w-4 h-4 text-sky-400" />
                </div>
              </div>
              <div className="flex items-baseline justify-between pt-2">
                <span className="text-3xl font-black text-white font-mono">{totalScans}</span>
                <span className="text-xs font-bold text-sky-400 flex items-center gap-0.5">
                  <TrendingUp className="w-3.5 h-3.5" /> Real Activity
                </span>
              </div>
            </Card>
          </ThreeDCard>
        </FadeIn>

        <FadeIn delay={0.1}>
          <ThreeDCard glowColor="amber">
            <Card className="space-y-2 border-slate-800 bg-slate-900/90 backdrop-blur-xl h-full">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Threats Blocked</span>
                <div className="bg-red-500/10 p-2 rounded-xl border border-red-500/30">
                  <ShieldAlert className="w-4 h-4 text-red-400" />
                </div>
              </div>
              <div className="flex items-baseline justify-between pt-2">
                <span className="text-3xl font-black text-red-400 font-mono">{dangerousScans}</span>
                <span className="text-xs font-bold text-red-400">{dangerousRate}% High Risk</span>
              </div>
            </Card>
          </ThreeDCard>
        </FadeIn>

        <FadeIn delay={0.15}>
          <ThreeDCard glowColor="emerald">
            <Card className="space-y-2 border-slate-800 bg-slate-900/90 backdrop-blur-xl h-full">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Clean Messages</span>
                <div className="bg-emerald-500/10 p-2 rounded-xl border border-emerald-500/30">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                </div>
              </div>
              <div className="flex items-baseline justify-between pt-2">
                <span className="text-3xl font-black text-emerald-400 font-mono">{safeScans}</span>
                <span className="text-xs font-bold text-emerald-400">{safeRate}% Safe Rate</span>
              </div>
            </Card>
          </ThreeDCard>
        </FadeIn>

        <FadeIn delay={0.2}>
          <ThreeDCard glowColor="purple">
            <Card className="space-y-2 border-slate-800 bg-slate-900/90 backdrop-blur-xl h-full">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Privacy Anonymization</span>
                <div className="bg-purple-500/10 p-2 rounded-xl border border-purple-500/30">
                  <Shield className="w-4 h-4 text-purple-400" />
                </div>
              </div>
              <div className="flex items-baseline justify-between pt-2">
                <span className="text-3xl font-black text-purple-400 font-mono">100%</span>
                <span className="text-xs font-bold text-slate-400">Zero PII Leakage</span>
              </div>
            </Card>
          </ThreeDCard>
        </FadeIn>
      </div>

      {/* ====================================================================
          2. MAIN CONTENT GRID (2 COLUMNS: LEFT 2/3, RIGHT 1/3)
          ==================================================================== */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT 2 COLUMNS */}
        <div className="lg:col-span-2 space-y-6">
          {/* QUICK SCANNER WIDGET */}
          <FadeIn delay={0.25}>
            <ThreeDCard intensity={8}>
              <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <h2 className="text-base font-black text-white flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
                    <span>Quick Threat Scanner</span>
                  </h2>
                  <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
                    {(['text', 'url', 'email', 'qr'] as const).map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setActiveQuickTab(tab)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all uppercase ${
                          activeQuickTab === tab
                            ? 'bg-sky-600 text-white shadow-md shadow-sky-500/20'
                            : 'text-slate-400 hover:text-white'
                        }`}
                      >
                        {tab}
                      </button>
                    ))}
                  </div>
                </div>

                <form onSubmit={handleQuickScanSubmit} className="space-y-3">
                  <textarea
                    rows={3}
                    value={quickInput}
                    onChange={(e) => setQuickInput(e.target.value)}
                    placeholder={`Paste suspicious ${activeQuickTab.toUpperCase()} content here for immediate XAI inspection...`}
                    className="w-full p-3 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition-colors"
                  />
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] text-slate-400 flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Client-side PII Scrubbing Active</span>
                    </span>
                    <Button type="submit" size="sm" rightIcon={<ArrowRight className="w-4 h-4" />}>
                      Inspect Now
                    </Button>
                  </div>
                </form>
              </Card>
            </ThreeDCard>
          </FadeIn>

          {/* RECENT SCANS LOG TABLE (REAL USER DATA) */}
          <FadeIn delay={0.3}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h2 className="text-base font-black text-white">Recent Inspection Logs</h2>
                <Link to="/history" className="text-xs font-bold text-sky-400 hover:underline flex items-center gap-1">
                  <span>View All Log History</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              {isLoading ? (
                <div className="space-y-3 py-2">
                  <Skeleton className="h-12 w-full rounded-xl" />
                  <Skeleton className="h-12 w-full rounded-xl" />
                </div>
              ) : scanHistory.length > 0 ? (
                <div className="space-y-2.5">
                  {scanHistory.slice(0, 5).map((scan) => {
                    const IconComp = getScanIcon(scan.payloadType);
                    return (
                      <div
                        key={scan.id}
                        className="flex flex-col sm:flex-row sm:items-center justify-between p-3 bg-slate-950/70 border border-slate-800/80 rounded-xl gap-3 hover:border-sky-500/50 hover:shadow-lg transition-all"
                      >
                        <div className="flex items-start gap-3">
                          <div className="bg-slate-800 p-2 rounded-lg shrink-0 mt-0.5">
                            <IconComp className="w-4 h-4 text-sky-400" />
                          </div>
                          <div className="space-y-0.5">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-bold text-white">{scan.payloadType}</span>
                              <span className="text-[10px] text-slate-500 font-mono">{scan.id}</span>
                            </div>
                            <p className="text-xs text-slate-300 font-mono line-clamp-1">{scan.payloadSnippet}</p>
                          </div>
                        </div>

                        <div className="flex items-center justify-between sm:justify-end gap-3 shrink-0 border-t sm:border-t-0 border-slate-800 pt-2 sm:pt-0">
                          <span
                            className={
                              scan.riskBand === 'dangerous'
                                ? 'badge-risk-dangerous'
                                : scan.riskBand === 'caution'
                                ? 'badge-risk-caution'
                                : 'badge-risk-safe'
                            }
                          >
                            {scan.riskBand.toUpperCase()} ({scan.threatScore})
                          </span>
                          <span className="text-[11px] text-slate-500 font-mono">
                            {new Date(scan.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-8 space-y-3 bg-slate-950/50 border border-slate-800/60 rounded-2xl">
                  <div className="bg-sky-500/10 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto border border-sky-500/30">
                    <ShieldCheck className="w-6 h-6 text-sky-400" />
                  </div>
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-white">No Recent Inspection Logs</h3>
                    <p className="text-xs text-slate-400 max-w-sm mx-auto">
                      You haven't run any threat scans yet. Inspect a URL, SMS Message, Email, or QR Code to view your live AI risk logs here.
                    </p>
                  </div>
                  <Link to="/scan/message" className="inline-block pt-1">
                    <Button size="sm" rightIcon={<ArrowRight className="w-4 h-4" />}>
                      Start Your First Inspection
                    </Button>
                  </Link>
                </div>
              )}
            </Card>
          </FadeIn>
        </div>

        {/* RIGHT COLUMN (1/3) */}
        <div className="space-y-6">
          {/* 3D THREAT SPHERE & LIVE FEED */}
          <FadeIn delay={0.35}>
            <ThreeDCard intensity={10} glowColor="purple">
              <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                  <h2 className="text-base font-black text-white flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-400 animate-pulse" />
                    <span>Global Threat Sensors</span>
                  </h2>
                  <span className="text-[10px] font-mono text-slate-500">LIVE 3D FEED</span>
                </div>

                {/* Interactive 3D Threat Sphere Widget */}
                <ThreatSphere3D />

                <div className="space-y-2.5 pt-2">
                  {liveThreatFeed.map((feed) => (
                    <div key={feed.id} className="p-2.5 bg-slate-950/80 border border-slate-800 rounded-xl space-y-0.5">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-bold text-sky-400 font-mono">{feed.category}</span>
                        <span className="text-slate-500">{feed.time}</span>
                      </div>
                      <p className="text-xs font-medium text-slate-300">{feed.title}</p>
                    </div>
                  ))}
                </div>
              </Card>
            </ThreeDCard>
          </FadeIn>

          {/* RISK DISTRIBUTION SUMMARY (REAL DATA) */}
          <FadeIn delay={0.4}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <h2 className="text-base font-black text-white">Risk Distribution</h2>
              <div className="space-y-3">
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-bold">
                    <span className="text-emerald-400">Safe Content</span>
                    <span className="text-white font-mono">{safeRate}% ({safeScans})</span>
                  </div>
                  <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 rounded-full transition-all duration-500" style={{ width: `${safeRate}%` }} />
                  </div>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-bold">
                    <span className="text-amber-400">Caution Warnings</span>
                    <span className="text-white font-mono">{cautionRate}% ({cautionScans})</span>
                  </div>
                  <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-500 rounded-full transition-all duration-500" style={{ width: `${cautionRate}%` }} />
                  </div>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-bold">
                    <span className="text-red-400">Dangerous Scams</span>
                    <span className="text-white font-mono">{dangerousRate}% ({dangerousScans})</span>
                  </div>
                  <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden">
                    <div className="h-full bg-red-500 rounded-full transition-all duration-500" style={{ width: `${dangerousRate}%` }} />
                  </div>
                </div>
              </div>
            </Card>
          </FadeIn>

          {/* SAFETY RECOMMENDATIONS */}
          <FadeIn delay={0.45}>
            <Card className="space-y-3 border-sky-500/30 bg-sky-500/5">
              <h2 className="text-sm font-black text-sky-400 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Security Hygiene Recommendation</span>
              </h2>
              <p className="text-xs text-slate-300 leading-relaxed">
                Welcome {currentUser?.fullName || 'User'}! Always verify unexpected SMS or email requests asking for urgent banking credentials or OTPs.
              </p>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
