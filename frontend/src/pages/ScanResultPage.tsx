import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  ArrowLeft,
  Copy,
  Download,
  Share2,
  Check,
  Clock,
  Brain,
  Zap,
  Globe,
  Lock,
  MessageSquare,
  Sparkles,
  FileText,
  AlertCircle,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { CinematicThreatGauge3D } from '../components/3d/CinematicThreatGauge3D';
import { ThreeDCard } from '../components/3d/ThreeDCard';

/**
 * GuardianAI Scan Result Detail Page Component
 * Purpose: Full XAI threat report breakdown with Risk Score Gauge, Confidence Level, Manipulative Triggers, Safe Reply Generator, and PDF Download.
 */

export const ScanResultPage: React.FC = () => {
  const { scanId = 'scn_8f92a1' } = useParams();
  const [copiedShare, setCopiedShare] = useState(false);
  const [copiedReply, setCopiedReply] = useState(false);
  const { showToast } = useToast();

  // Mock Comprehensive Scan Data
  const scanData = {
    scanId,
    timestamp: 'July 28, 2026 at 11:42 PM',
    payloadType: 'SMS Smishing',
    threatScore: 92,
    riskBand: 'dangerous' as const,
    confidence: 98.4,
    executionMs: 1420,
    originalText:
      'URGENT: Your Bank of America account is locked due to suspicious activity. Verify immediately at http://paypa1-check.com or your account will be permanently suspended.',
    plainRationale:
      'This message exhibits high-severity smishing characteristics. It combines artificial urgency ("account is locked") with an unauthorized typosquatted URL mimicking PayPal.',
    manipulationTriggers: [
      { tactic: 'Artificial Urgency', severity: 'High', description: 'Forces immediate panic to bypass critical thinking.' },
      { tactic: 'Typosquatting Spoof', severity: 'Critical', description: 'Replaces "l" with "1" in fake domain (paypa1-check.com).' },
      { tactic: 'Fear / Account Closure Threat', severity: 'High', description: 'Threatens permanent account suspension.' },
    ],
    suspiciousUrls: [
      {
        url: 'http://paypa1-check.com',
        tld: '.com',
        domainAge: '2 days old (Zero-Day)',
        sslCert: 'None (Unencrypted HTTP)',
        homoglyph: "Replaces 'l' with '1'",
      },
    ],
    remediations: [
      'Do not click the link or enter any login credentials.',
      'Block the sender number immediately in your phone settings.',
      'Log in directly to your official bank website by typing the address manually in your browser.',
      'Report this SMS to your carrier by forwarding it to 7726 (SPAM).',
    ],
    safeReply:
      'I have flagged this message as a phishing attempt and will not click the link. I am reporting this number to official bank fraud support.',
    timeline: [
      { step: 'Payload Received & PII Scrubbed', time: '11:42:01.000 PM', status: 'completed' },
      { step: 'Model Dual-Pass Analysis', time: '11:42:01.420 PM', status: 'completed' },
      { step: 'XAI Signal Rationale Generated', time: '11:42:01.980 PM', status: 'completed' },
      { step: 'Report Sealed & Cached', time: '11:42:02.420 PM', status: 'completed' },
    ],
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopiedShare(true);
    showToast('success', 'Report Link Copied', 'Share link copied to clipboard.');
    setTimeout(() => setCopiedShare(false), 2000);
  };

  const handleCopyReply = () => {
    navigator.clipboard.writeText(scanData.safeReply);
    setCopiedReply(true);
    showToast('success', 'Safe Reply Copied', 'Copied safe refusal message to clipboard.');
    setTimeout(() => setCopiedReply(false), 2000);
  };

  const handleDownloadPdf = () => {
    showToast('info', 'Generating PDF Report', 'Preparing print-ready threat analysis report...');
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Navigation Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-3">
          <Link to="/history" className="p-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 rounded-xl text-slate-300 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-black text-white">Threat Analysis Report</h1>
              <span className="font-mono text-xs text-sky-400 font-bold bg-sky-500/10 border border-sky-500/30 px-2 py-0.5 rounded-full">
                {scanData.scanId}
              </span>
            </div>
            <p className="text-xs text-slate-400">{scanData.timestamp} • Executed in {scanData.executionMs}ms</p>
          </div>
        </div>

        {/* Share & Download Buttons */}
        <div className="flex items-center gap-2">
          <Button variant="secondary" size="sm" onClick={handleShare} leftIcon={<Share2 className="w-4 h-4" />}>
            {copiedShare ? 'Copied Link' : 'Share Report'}
          </Button>
          <Button size="sm" onClick={handleDownloadPdf} leftIcon={<Download className="w-4 h-4" />}>
            Download PDF
          </Button>
        </div>
      </div>

      {/* ====================================================================
          1. RISK SCORE GAUGE & AI CONFIDENCE BANNER
          ==================================================================== */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* 3D Cinematic Risk Index Gauge Card */}
        <ThreeDCard glowColor="amber" intensity={12}>
          <Card className="border-2 border-red-500/60 bg-slate-900/90 backdrop-blur-xl space-y-4 flex flex-col justify-between h-full">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Threat Index Score</span>
              <span className="badge-risk-dangerous">DANGEROUS</span>
            </div>

            {/* 3D Cinematic Circular Risk Gauge */}
            <CinematicThreatGauge3D score={scanData.threatScore} riskBand={scanData.riskBand} />

            <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-800">
              <span className="text-slate-400">AI Confidence SLA:</span>
              <span className="font-mono font-bold text-emerald-400">{scanData.confidence}% Verified</span>
            </div>
          </Card>
        </ThreeDCard>

        {/* Executive Summary Card (2 Columns Width) */}
        <Card className="md:col-span-2 space-y-4 border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-base font-black text-white flex items-center gap-2">
              <Brain className="w-5 h-5 text-sky-400" />
              <span>Plain Language Rationale</span>
            </h2>
            <span className="text-xs text-slate-400 font-mono">Payload: {scanData.payloadType}</span>
          </div>

          <p className="text-sm text-slate-200 leading-relaxed font-medium bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            {scanData.plainRationale}
          </p>

          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <Lock className="w-4 h-4 text-emerald-400" />
              <span>Zero-Knowledge PII Anonymized</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Zap className="w-4 h-4 text-amber-400" />
              <span>Sub-1.8s SLA Model</span>
            </div>
          </div>
        </Card>
      </div>

      {/* ====================================================================
          2. DETAILED XAI HIGHLIGHTS & MANIPULATION TACTICS
          ==================================================================== */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: TEXT VIEWER & MANIPULATION (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Highlighted Suspicious Words Viewer */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
              <FileText className="w-4 h-4 text-sky-400" />
              <span>Inspected Text Payload & Highlights</span>
            </h2>

            <div className="p-4 bg-slate-900 rounded-xl border border-slate-800 font-mono text-sm leading-relaxed text-slate-200">
              <span className="xai-highlight-urgency">URGENT:</span> Your Bank of America account is locked due to suspicious activity. Verify immediately at <span className="xai-highlight-typosquat">http://paypa1-check.com</span> or your account will be permanently suspended.
            </div>
          </Card>

          {/* Psychological Manipulation Detected */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span>Psychological Manipulation Detected</span>
            </h2>

            <div className="space-y-3">
              {scanData.manipulationTriggers.map((trigger, idx) => (
                <div key={idx} className="p-3 bg-slate-900 border border-slate-800 rounded-xl flex items-start justify-between gap-3">
                  <div className="space-y-0.5">
                    <span className="text-xs font-black text-white">{trigger.tactic}</span>
                    <p className="text-xs text-slate-300">{trigger.description}</p>
                  </div>
                  <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 shrink-0">
                    {trigger.severity}
                  </span>
                </div>
              ))}
            </div>
          </Card>

          {/* Suspicious URLs Analysis */}
          <Card className="space-y-4 border-slate-800">
            <h2 className="text-base font-black text-white flex items-center gap-2 border-b border-slate-800 pb-3">
              <Globe className="w-4 h-4 text-sky-400" />
              <span>Extracted Suspicious Links</span>
            </h2>

            {scanData.suspiciousUrls.map((item, idx) => (
              <div key={idx} className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-3">
                <div className="font-mono text-xs font-bold text-red-400 break-all">{item.url}</div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                  <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-slate-500 text-[10px]">Domain Age</span>
                    <p className="font-bold text-red-400">{item.domainAge}</p>
                  </div>
                  <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-slate-500 text-[10px]">SSL Certificate</span>
                    <p className="font-bold text-amber-400">{item.sslCert}</p>
                  </div>
                  <div className="p-2 bg-slate-950 rounded-lg border border-slate-800 col-span-2 sm:col-span-1">
                    <span className="text-slate-500 text-[10px]">Homoglyph Check</span>
                    <p className="font-bold text-red-400">{item.homoglyph}</p>
                  </div>
                </div>
              </div>
            ))}
          </Card>
        </div>

        {/* RIGHT COLUMN: SAFE REPLY & TIMELINE (1/3 Width) */}
        <div className="space-y-6">
          {/* SAFE REPLY GENERATOR */}
          <FadeIn delay={0.2}>
            <Card className="space-y-3 border-sky-500/30 bg-sky-500/5">
              <div className="flex items-center justify-between border-b border-sky-500/20 pb-2">
                <h3 className="text-sm font-black text-sky-400 flex items-center gap-1.5">
                  <MessageSquare className="w-4 h-4" />
                  <span>AI Suggested Safe Reply</span>
                </h3>
                <Button variant="secondary" size="sm" onClick={handleCopyReply} leftIcon={<Copy className="w-3.5 h-3.5" />}>
                  {copiedReply ? 'Copied' : 'Copy'}
                </Button>
              </div>
              <p className="text-xs text-slate-200 bg-slate-900 p-3 rounded-xl border border-slate-800 font-mono leading-relaxed">
                "{scanData.safeReply}"
              </p>
            </Card>
          </FadeIn>

          {/* INSPECTION TIMELINE */}
          <FadeIn delay={0.3}>
            <Card className="space-y-3 border-slate-800">
              <h3 className="text-sm font-black text-white flex items-center gap-2 border-b border-slate-800 pb-2">
                <Clock className="w-4 h-4 text-sky-400" />
                <span>Execution Timeline</span>
              </h3>

              <div className="space-y-3 pl-2 border-l-2 border-slate-800">
                {scanData.timeline.map((item, idx) => (
                  <div key={idx} className="relative pl-4 space-y-0.5">
                    <div className="absolute -left-[13px] top-1 w-2.5 h-2.5 rounded-full bg-sky-400 border-2 border-slate-950" />
                    <p className="text-xs font-bold text-white">{item.step}</p>
                    <p className="text-[10px] font-mono text-slate-500">{item.time}</p>
                  </div>
                ))}
              </div>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
