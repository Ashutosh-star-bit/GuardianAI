import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageSquare,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Lock,
  Copy,
  Check,
  RefreshCw,
  Clock,
  HelpCircle,
  Zap,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { scanService, ScanResultData } from '../services/api/scanService';
import { ThreeDCard } from '../components/3d/ThreeDCard';
import { CyberRadar3D } from '../components/3d/CyberRadar3D';

/**
 * GuardianAI Message & SMS Smishing Inspection Page Component
 * Purpose: Dedicated tool for inspecting suspicious text messages, SMS smishing, and chat payloads with XAI highlights.
 */

export const MessageScanPage: React.FC = () => {
  const { incrementScanCount, addScanRecord } = useAuth();
  const [message, setMessage] = useState('');
  const [zeroKnowledge, setZeroKnowledge] = useState(true);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResultData | null>(null);
  const [copied, setCopied] = useState(false);
  const { showToast } = useToast();

  const MAX_CHARS = 5000;

  // Preset Sample Scam Payloads
  const sampleMessages = [
    {
      title: 'Urgent Bank Account Lock',
      text: 'URGENT: Your Bank of America account is locked due to suspicious activity. Verify immediately at http://paypa1-check.com or your account will be permanently suspended.',
      type: 'Dangerous',
    },
    {
      title: 'Package Delivery SMS',
      text: 'FedEx: Your package delivery #88219 has a pending unpaid customs fee of $2.45. Pay now to avoid return: http://fedex-customs-pay.top',
      type: 'Caution',
    },
    {
      title: 'Benign Meeting Confirmation',
      text: 'Hi John, confirming our project sync tomorrow at 3:00 PM in Conference Room B. See you then!',
      type: 'Safe',
    },
  ];

  const handleSelectSample = (sampleText: string) => {
    setMessage(sampleText);
    showToast('info', 'Sample Loaded', 'Preset message loaded into inspector.');
  };

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim().length < 3) {
      showToast('error', 'Payload Too Short', 'Please enter at least 3 characters to scan.');
      return;
    }

    const canScan = incrementScanCount();
    if (!canScan) {
      showToast(
        'error',
        'Monthly Scan Limit Reached (15/15)',
        'You have reached your 15 Free Scans limit for this month. Upgrade to Pro ($4.99/mo) for unlimited AI scans!'
      );
      return;
    }

    setIsScanning(true);
    setScanResult(null);

    try {
      const result = await scanService.scanText({
        payload: message,
        zeroKnowledge,
      });
      setScanResult(result);

      // Record into real scan history
      addScanRecord({
        payloadType: 'Text/SMS',
        payloadSnippet: message,
        threatScore: result.threatScore,
        riskBand: result.riskBand,
        plainRationale: result.plainRationale,
        remediation: result.remediation,
        executionMs: result.executionMs,
      });

      showToast(
        result.riskBand === 'dangerous' ? 'error' : result.riskBand === 'caution' ? 'info' : 'success',
        'Scan Completed',
        `Risk Score: ${result.threatScore}/100 (${result.riskBand.toUpperCase()})`
      );
    } catch (err) {
      showToast('error', 'Scan Error', 'An error occurred during analysis. Please try again.');
    } finally {
      setIsScanning(false);
    }
  };

  const handleCopyRemediation = () => {
    if (!scanResult) return;
    const textToCopy = `GuardianAI Threat Report (${scanResult.scanId})\nRisk Band: ${scanResult.riskBand.toUpperCase()} (${scanResult.threatScore}/100)\n\nRationale:\n${scanResult.plainRationale}\n\nRecommended Actions:\n${scanResult.remediation.map((r, i) => `${i + 1}. ${r}`).join('\n')}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    showToast('success', 'Copied to Clipboard', 'Report summary copied.');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Page Title Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <MessageSquare className="w-4 h-4" />
          <span>Message Inspection Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">SMS & Message Smishing Inspector</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Inspect suspicious SMS, WhatsApp, and chat messages. Our Explainable AI reveals manipulative psychological triggers.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: INPUT FORM & RESULT (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          {/* 3D HOLOGRAPHIC AI RADAR & INPUT CARD */}
          <ThreeDCard glowColor="cyan" intensity={10}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h2 className="text-base font-black text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
                  <span>Input Message Payload</span>
                </h2>
                <span className="text-xs text-slate-400 font-mono">
                  {message.length} / {MAX_CHARS} chars
                </span>
              </div>

              <form onSubmit={handleScan} className="space-y-4">
              <textarea
                rows={6}
                value={message}
                maxLength={MAX_CHARS}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Paste suspicious text message, SMS, or chat payload here (e.g. URGENT: Your account is locked!)..."
                className="w-full p-4 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition-colors"
              />

              {/* Controls Bar */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-300 font-medium">
                  <input
                    type="checkbox"
                    checked={zeroKnowledge}
                    onChange={(e) => setZeroKnowledge(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-700 text-sky-500 focus:ring-sky-500 bg-slate-900"
                  />
                  <span className="flex items-center gap-1">
                    <Lock className="w-3.5 h-3.5 text-emerald-400" />
                    Zero-Knowledge PII Anonymization
                  </span>
                </label>

                <div className="flex items-center gap-2">
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setMessage('');
                      setScanResult(null);
                    }}
                  >
                    Clear
                  </Button>
                  <Button
                    type="submit"
                    isLoading={isScanning}
                    size="sm"
                    className="shadow-sky-500/20 shadow-lg"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    Run XAI Inspection
                  </Button>
                </div>
              </div>
            </form>

            {/* PRESET SAMPLES PICKER */}
            <div className="pt-3 border-t border-slate-800 space-y-2">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Try Preset Test Samples:</span>
              <div className="flex flex-wrap gap-2">
                {sampleMessages.map((sample, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSelectSample(sample.text)}
                    className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition-colors text-left"
                  >
                    <span className="font-bold text-sky-400 mr-1.5">[{sample.type}]</span>
                    <span>{sample.title}</span>
                  </button>
                ))}
              </div>
            </div>
          </Card>
        </ThreeDCard>

          {/* XAI INSPECTION RESULT DISPLAY CARD */}
          <AnimatePresence>
            {scanResult && (
              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -16 }}
                transition={{ duration: 0.3 }}
              >
                <Card
                  className={`space-y-6 border-2 ${
                    scanResult.riskBand === 'dangerous'
                      ? 'border-red-500/60 bg-red-950/10'
                      : scanResult.riskBand === 'caution'
                      ? 'border-amber-500/60 bg-amber-950/10'
                      : 'border-emerald-500/60 bg-emerald-950/10'
                  }`}
                >
                  {/* Result Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800/80 pb-4 gap-3">
                    <div className="flex items-center gap-3">
                      <div
                        className={`p-2.5 rounded-xl border ${
                          scanResult.riskBand === 'dangerous'
                            ? 'bg-red-500/10 border-red-500/40 text-red-400'
                            : scanResult.riskBand === 'caution'
                            ? 'bg-amber-500/10 border-amber-500/40 text-amber-400'
                            : 'bg-emerald-500/10 border-emerald-500/40 text-emerald-400'
                        }`}
                      >
                        {scanResult.riskBand === 'dangerous' ? (
                          <ShieldAlert className="w-6 h-6" />
                        ) : scanResult.riskBand === 'caution' ? (
                          <AlertTriangle className="w-6 h-6" />
                        ) : (
                          <ShieldCheck className="w-6 h-6" />
                        )}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-black text-white">XAI Threat Assessment</h3>
                          <span
                            className={
                              scanResult.riskBand === 'dangerous'
                                ? 'badge-risk-dangerous'
                                : scanResult.riskBand === 'caution'
                                ? 'badge-risk-caution'
                                : 'badge-risk-safe'
                            }
                          >
                            {scanResult.riskBand.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 font-mono">
                          ID: {scanResult.scanId} • Executed in {scanResult.executionMs}ms
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <span className="text-2xl font-black text-white">{scanResult.threatScore}</span>
                        <span className="text-xs text-slate-400"> / 100</span>
                        <p className="text-[10px] text-slate-500 font-bold uppercase">Threat Index</p>
                      </div>
                      <Button variant="secondary" size="sm" onClick={handleCopyRemediation} leftIcon={<Copy className="w-3.5 h-3.5" />}>
                        {copied ? 'Copied' : 'Share'}
                      </Button>
                    </div>
                  </div>

                  {/* Plain Language Rationale */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Plain Language Explanation</h4>
                    <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl text-sm text-slate-200 leading-relaxed font-medium">
                      {scanResult.plainRationale}
                    </div>
                  </div>

                  {/* Text Manipulative Highlights */}
                  {scanResult.highlights && scanResult.highlights.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Manipulative Triggers Flagged</h4>
                      <div className="space-y-2">
                        {scanResult.highlights.map((item, idx) => (
                          <div key={idx} className="p-3 bg-slate-900 border border-slate-800 rounded-xl flex items-start gap-3">
                            <span className="text-xs font-mono font-bold text-amber-400 bg-amber-950/80 px-2 py-0.5 rounded border border-amber-800 shrink-0 mt-0.5">
                              {item.type}
                            </span>
                            <div className="space-y-0.5">
                              <p className="text-xs font-bold text-white font-mono">"{item.text}"</p>
                              <p className="text-xs text-slate-300">{item.reason}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommended Remediation Steps */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Step-by-Step Safety Advice</h4>
                    <div className="space-y-2">
                      {scanResult.remediation.map((step, idx) => (
                        <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-200 bg-slate-900 p-3 rounded-xl border border-slate-800">
                          <Check className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                          <span>{step}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* RIGHT COLUMN: TIPS & HISTORY (1/3 Width) */}
        <div className="space-y-6">
          {/* SAFETY TIPS */}
          <FadeIn delay={0.2}>
            <Card className="space-y-3 border-slate-800">
              <h3 className="text-sm font-black text-white flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-sky-400" />
                <span>Smishing Detection Rules</span>
              </h3>
              <ul className="space-y-2.5 text-xs text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Artificial Urgency:</strong> Messages demanding immediate action within 24 hours are almost always scams.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Spoofed Links:</strong> Inspect links carefully for typos (e.g. <code>paypa1.com</code> instead of <code>paypal.com</code>).</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Unsolicited OTPs:</strong> Never share 6-digit verification codes over text or phone calls.</span>
                </li>
              </ul>
            </Card>
          </FadeIn>

          {/* PRIVACY GUARANTEE */}
          <FadeIn delay={0.3}>
            <Card className="space-y-2 border-emerald-500/30 bg-emerald-500/5">
              <h3 className="text-xs font-black text-emerald-400 flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5" />
                <span>Zero-Knowledge Protection</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                All PII (names, card numbers, SSNs, phone numbers) is scrubbed locally inside your browser before any network transmission.
              </p>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
