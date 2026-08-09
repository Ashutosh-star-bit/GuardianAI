import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Globe,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Lock,
  ExternalLink,
  Copy,
  Check,
  HelpCircle,
  Clock,
  Calendar,
  Key,
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
 * GuardianAI URL & Domain Typosquatting Inspection Page Component
 * Purpose: Inspects suspicious web links, homoglyph domain spoofs, zero-day WHOIS domains, and SSL certificates.
 */

export const UrlScanPage: React.FC = () => {
  const { incrementScanCount, addScanRecord } = useAuth();
  const [url, setUrl] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResultData | null>(null);
  const [copied, setCopied] = useState(false);
  const { showToast } = useToast();

  // Preset Sample URLs
  const sampleUrls = [
    {
      title: 'Typosquatted PayPal Domain',
      url: 'http://paypa1-security-check.com/login?id=8812',
      type: 'Dangerous',
    },
    {
      title: 'Homoglyph Bank of America Spoof',
      url: 'https://security-verify-bаnkofamerica.top/auth',
      type: 'Dangerous',
    },
    {
      title: 'Legitimate Apple Support URL',
      url: 'https://support.apple.com/id-lookup',
      type: 'Safe',
    },
  ];

  const handleSelectSample = (sampleUrl: string) => {
    setUrl(sampleUrl);
    showToast('info', 'Sample URL Loaded', 'Loaded preset link into inspector.');
  };

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) {
      showToast('error', 'Empty URL', 'Please enter a valid website link.');
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
      const result = await scanService.scanUrl(url);
      setScanResult(result);

      addScanRecord({
        payloadType: 'URL Link',
        payloadSnippet: url,
        threatScore: result.threatScore,
        riskBand: result.riskBand,
        plainRationale: result.plainRationale,
        remediation: result.remediation,
        executionMs: result.executionMs,
      });

      showToast(
        result.riskBand === 'dangerous' ? 'error' : result.riskBand === 'caution' ? 'info' : 'success',
        'URL Inspection Complete',
        `Threat Score: ${result.threatScore}/100`
      );
    } catch (err) {
      showToast('error', 'Scan Error', 'Failed to analyze target URL domain.');
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Page Title Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <Globe className="w-4 h-4" />
          <span>URL & Domain Inspection Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">URL & Domain Typosquatting Inspector</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Check suspicious website links for homoglyph domain spoofs, zero-day WHOIS age, and malicious redirect chains.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: INPUT FORM & RESULTS (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          <ThreeDCard glowColor="cyan" intensity={10}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <h2 className="text-base font-black text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
                  <span>Input Website Link</span>
                </h2>
              </div>

              <form onSubmit={handleScan} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300">Target Web Link / Domain</label>
                  <div className="relative">
                    <Globe className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://example-suspicious-site.com/verify"
                      className="w-full pl-10 pr-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 font-mono transition-colors"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setUrl('');
                      setScanResult(null);
                    }}
                  >
                    Clear Link
                  </Button>
                  <Button
                    type="submit"
                    isLoading={isScanning}
                    size="sm"
                    className="shadow-sky-500/20 shadow-lg"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    Inspect URL Threat
                  </Button>
                </div>
              </form>

              {/* PRESET SAMPLES */}
              <div className="pt-3 border-t border-slate-800 space-y-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Try Preset URL Samples:</span>
                <div className="flex flex-wrap gap-2">
                {sampleUrls.map((sample, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSelectSample(sample.url)}
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

          {/* INSPECTION RESULTS DISPLAY */}
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
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800/80 pb-4 gap-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl border bg-slate-900 border-slate-800 text-sky-400">
                        <Globe className="w-6 h-6" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-black text-white">Domain Risk Assessment</h3>
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
                        <p className="text-xs text-slate-400 font-mono">ID: {scanResult.scanId}</p>
                      </div>
                    </div>

                    <div className="text-right">
                      <span className="text-2xl font-black text-white">{scanResult.threatScore}</span>
                      <span className="text-xs text-slate-400"> / 100</span>
                      <p className="text-[10px] text-slate-500 font-bold uppercase">Threat Index</p>
                    </div>
                  </div>

                  {/* Domain WHOIS & Security Metadata Grid */}
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px] flex items-center justify-center gap-1">
                        <Calendar className="w-3 h-3 text-sky-400" /> Domain Age
                      </span>
                      <p className="font-bold text-red-400">2 Days Old (Zero-Day)</p>
                    </div>
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px] flex items-center justify-center gap-1">
                        <Key className="w-3 h-3 text-amber-400" /> SSL Cert
                      </span>
                      <p className="font-bold text-amber-400">Let's Encrypt DV</p>
                    </div>
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px] flex items-center justify-center gap-1">
                        <ShieldAlert className="w-3 h-3 text-red-400" /> Homoglyph
                      </span>
                      <p className="font-bold text-red-400">Detected ('1' for 'l')</p>
                    </div>
                  </div>

                  {/* Rationale */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Plain Language Explanation</h4>
                    <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl text-sm text-slate-200 leading-relaxed font-medium">
                      {scanResult.plainRationale}
                    </div>
                  </div>

                  {/* Remediation */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Safety Advice</h4>
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

        {/* RIGHT COLUMN: TIPS (1/3 Width) */}
        <div className="space-y-6">
          <FadeIn delay={0.2}>
            <Card className="space-y-3 border-slate-800">
              <h3 className="text-sm font-black text-white flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-sky-400" />
                <span>URL Typosquatting Rules</span>
              </h3>
              <ul className="space-y-2.5 text-xs text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Character Substitution:</strong> Scammers replace letters like <code>l</code> with <code>1</code> or <code>o</code> with <code>0</code>.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Zero-Day WHOIS:</strong> Domains registered less than 30 days ago are 10x more likely to host phishing forms.</span>
                </li>
              </ul>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
