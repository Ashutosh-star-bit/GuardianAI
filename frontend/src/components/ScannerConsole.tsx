import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, AlertTriangle, Lock, Send, LogIn, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { scanService, ScanResultData } from '../services/api/scanService';
import { CyberRadar3D } from './3d/CyberRadar3D';

export const ScannerConsole: React.FC = () => {
  const { isAuthenticated, incrementScanCount, addScanRecord } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [inputText, setInputText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [scanResult, setScanResult] = useState<ScanResultData | null>(null);

  const handleScan = async () => {
    if (!inputText.trim()) {
      showToast('error', 'Empty Message', 'Please enter or paste a suspicious message to analyze.');
      return;
    }

    if (!isAuthenticated) {
      showToast('info', 'Sign In Required', 'Please sign in or register to execute full AI threat analysis.');
      navigate('/login');
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

    setIsLoading(true);
    setScanResult(null);

    try {
      const result = await scanService.scanText({ payload: inputText });
      setScanResult(result);

      addScanRecord({
        payloadType: 'Text/SMS',
        payloadSnippet: inputText,
        threatScore: result.threatScore,
        riskBand: result.riskBand,
        plainRationale: result.plainRationale,
        remediation: result.remediation,
        executionMs: result.executionMs,
      });

      showToast('success', 'Analysis Complete', `Threat Score: ${result.threatScore}/100`);
    } catch (err) {
      showToast('error', 'Scan Error', 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-2xl max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-xl font-black text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <span>Interactive Live Threat Inspector</span>
          </h3>
          <p className="text-xs text-slate-400">
            Zero-Knowledge Privacy: PII is scrubbed in your browser before processing.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1.5 rounded-full">
          <Lock className="w-3.5 h-3.5" />
          <span>Privacy Scrubbing Active</span>
        </div>
      </div>

      <div className="space-y-4">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste suspicious text message, email snippet, or URL link here (e.g. URGENT: Your bank account is suspended. Verify at http://paypa1-verify.top)..."
          rows={4}
          className="w-full bg-slate-950 border border-slate-800 focus:border-sky-400 text-white rounded-2xl p-4 text-sm outline-none transition-all resize-none placeholder-slate-500"
        />

        <div className="flex flex-col sm:flex-row justify-between items-center gap-3">
          <p className="text-xs text-slate-400">
            {!isAuthenticated ? (
              <span className="text-amber-400 font-bold">⚠️ Sign in required to execute AI scans</span>
            ) : (
              <span>15 Free Scans / Month active</span>
            )}
          </p>

          <button
            onClick={handleScan}
            disabled={isLoading}
            className="w-full sm:w-auto px-6 py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-sm rounded-xl transition-all shadow-lg shadow-sky-500/20 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <span>Analyzing Payload...</span>
            ) : !isAuthenticated ? (
              <>
                <LogIn className="w-4 h-4" />
                <span>Sign In to Analyze Message</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Analyze Message</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Render Scan Results */}
      {scanResult && (
        <div className="pt-4 border-t border-slate-800 space-y-4 animate-fade-in">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Analysis Report</span>
            <span
              className={`px-3 py-1 rounded-full text-xs font-black uppercase ${
                scanResult.riskBand === 'dangerous'
                  ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                  : scanResult.riskBand === 'caution'
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                  : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
              }`}
            >
              {scanResult.riskBand} ({scanResult.threatScore}/100)
            </span>
          </div>

          <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 space-y-2">
            <p className="text-sm text-slate-200">{scanResult.plainRationale}</p>
          </div>
        </div>
      )}
    </div>
  );
};
