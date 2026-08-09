import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Mail,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Lock,
  Paperclip,
  CheckCircle2,
  XCircle,
  UploadCloud,
  FileText,
  Copy,
  Check,
  HelpCircle,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { scanService, ScanResultData } from '../services/api/scanService';
import { ThreeDCard } from '../components/3d/ThreeDCard';

/**
 * GuardianAI Email Header & BEC Inspection Page Component
 * Purpose: Analyzes email senders, subjects, bodies, raw headers, and attachments for Business Email Compromise (BEC) and spoofing.
 */

export const EmailScanPage: React.FC = () => {
  const [pasteRawHeaders, setPasteRawHeaders] = useState(false);
  const [sender, setSender] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [rawHeaders, setRawHeaders] = useState('');
  const [attachment, setAttachment] = useState<File | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<ScanResultData | null>(null);
  const [copied, setCopied] = useState(false);
  const { showToast } = useToast();

  // Preset BEC Sample Emails
  const sampleEmails = [
    {
      title: 'Executive BEC Wire Transfer',
      sender: 'ceo-office@company-corp.xyz',
      subject: 'URGENT: Confidential Wire Transfer Request #9921',
      body: 'I am currently in an all-day board meeting. Please process an urgent wire transfer of $48,500 to the attached vendor account before 3:00 PM today. Do not call me as I am unable to answer phone calls.',
      type: 'Dangerous',
    },
    {
      title: 'Payroll Direct Deposit Update',
      sender: 'hr-support@payroll-verify.top',
      subject: 'Action Required: Verify Employee Direct Deposit Information',
      body: 'Your payroll account has a pending deposit hold. Please click the link to confirm your bank account routing number.',
      type: 'Caution',
    },
  ];

  const handleSelectSample = (sample: typeof sampleEmails[0]) => {
    setSender(sample.sender);
    setSubject(sample.subject);
    setBody(sample.body);
    showToast('info', 'Sample Email Loaded', 'Loaded BEC email payload.');
  };

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (pasteRawHeaders) {
      if (!rawHeaders.trim()) {
        showToast('error', 'Empty Headers', 'Please paste raw RFC 822 email headers.');
        return;
      }
    } else {
      if (!sender.trim() || !body.trim()) {
        showToast('error', 'Missing Fields', 'Please enter sender email address and email body content.');
        return;
      }
    }

    setIsScanning(true);
    setScanResult(null);

    const payloadText = pasteRawHeaders
      ? rawHeaders
      : `From: ${sender}\nSubject: ${subject}\n\n${body}`;

    try {
      const result = await scanService.scanText({ payload: payloadText });
      setScanResult(result);
      showToast(
        result.riskBand === 'dangerous' ? 'error' : result.riskBand === 'caution' ? 'info' : 'success',
        'Email Inspection Complete',
        `Threat Index: ${result.threatScore}/100`
      );
    } catch (err) {
      showToast('error', 'Inspection Error', 'Failed to analyze email payload.');
    } finally {
      setIsScanning(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAttachment(e.target.files[0]);
      showToast('success', 'File Attached', `Attached: ${e.target.files[0].name}`);
    }
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Page Header */}
      <div className="border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <Mail className="w-4 h-4" />
          <span>Email & Header Inspection Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Email BEC & Header Inspector</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Detect Executive BEC wire fraud, display-name spoofing, and malicious attachments before taking action.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* LEFT COLUMN: INPUT FORM & RESULTS (2/3 Width) */}
        <div className="lg:col-span-2 space-y-6">
          <ThreeDCard glowColor="cyan" intensity={10}>
            <Card className="space-y-4 border-slate-800 bg-slate-900/90 backdrop-blur-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h2 className="text-base font-black text-white flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-sky-400" />
                <span>Email Payload Inspector</span>
              </h2>

              {/* Mode Toggle Button */}
              <button
                type="button"
                onClick={() => setPasteRawHeaders(!pasteRawHeaders)}
                className="text-xs font-bold text-sky-400 hover:underline flex items-center gap-1"
              >
                <span>{pasteRawHeaders ? 'Switch to Form Mode' : 'Paste Raw RFC 822 Headers'}</span>
              </button>
            </div>

            <form onSubmit={handleScan} className="space-y-4">
              {pasteRawHeaders ? (
                /* Raw RFC 822 Headers Mode */
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-300">Raw Email Headers & Body</label>
                  <textarea
                    rows={8}
                    value={rawHeaders}
                    onChange={(e) => setRawHeaders(e.target.value)}
                    placeholder="Paste raw email headers (e.g., Received: from mail.example.com, SPF=pass, DKIM=fail)..."
                    className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-xs font-mono text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  />
                </div>
              ) : (
                /* Structured Form Mode */
                <div className="space-y-3">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-300">Sender Email Address</label>
                      <input
                        type="email"
                        value={sender}
                        onChange={(e) => setSender(e.target.value)}
                        placeholder="e.g. ceo-office@company-corp.xyz"
                        className="w-full p-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-300">Subject Line</label>
                      <input
                        type="text"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                        placeholder="e.g. URGENT: Confidential Wire Transfer"
                        className="w-full p-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                      />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-300">Email Body Message</label>
                    <textarea
                      rows={5}
                      value={body}
                      onChange={(e) => setBody(e.target.value)}
                      placeholder="Paste the email content body here..."
                      className="w-full p-3 bg-slate-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                    />
                  </div>

                  {/* Attachment Upload Zone */}
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-300">Attachment Inspection (.eml, .pdf, .docx)</label>
                    <div className="border-2 border-dashed border-slate-800 hover:border-sky-500/50 rounded-xl p-4 text-center cursor-pointer bg-slate-900/50 transition-colors relative">
                      <input
                        type="file"
                        onChange={handleFileUpload}
                        className="absolute inset-0 opacity-0 cursor-pointer"
                        accept=".eml,.msg,.pdf,.docx"
                      />
                      {attachment ? (
                        <div className="flex items-center justify-center gap-2 text-sky-400 font-bold text-xs">
                          <FileText className="w-4 h-4" />
                          <span>{attachment.name} ({(attachment.size / 1024).toFixed(1)} KB)</span>
                        </div>
                      ) : (
                        <div className="space-y-1 text-slate-400">
                          <UploadCloud className="w-6 h-6 mx-auto text-slate-500" />
                          <p className="text-xs font-medium">Click or drag email attachment file to upload</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Submit Buttons */}
              <div className="flex items-center justify-between pt-2">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={() => {
                    setSender('');
                    setSubject('');
                    setBody('');
                    setRawHeaders('');
                    setAttachment(null);
                    setScanResult(null);
                  }}
                >
                  Clear Form
                </Button>
                <Button
                  type="submit"
                  isLoading={isScanning}
                  size="sm"
                  className="shadow-sky-500/20 shadow-lg"
                  rightIcon={<ArrowRight className="w-4 h-4" />}
                >
                  Analyze Email Threat
                </Button>
              </div>
            </form>

            {/* PRESET SAMPLES */}
            <div className="pt-3 border-t border-slate-800 space-y-2">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Try Sample BEC Emails:</span>
              <div className="flex flex-wrap gap-2">
                {sampleEmails.map((sample, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSelectSample(sample)}
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
                        <Mail className="w-6 h-6" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-black text-white">BEC Threat Assessment</h3>
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

                  {/* Authentication Protocol Badges */}
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px]">SPF Record</span>
                      <p className="font-bold text-red-400 flex items-center justify-center gap-1">
                        <XCircle className="w-3.5 h-3.5" /> SOFTFAIL
                      </p>
                    </div>
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px]">DKIM Signature</span>
                      <p className="font-bold text-red-400 flex items-center justify-center gap-1">
                        <XCircle className="w-3.5 h-3.5" /> FAIL
                      </p>
                    </div>
                    <div className="p-2 bg-slate-900 rounded-lg border border-slate-800 space-y-0.5">
                      <span className="text-slate-400 font-mono text-[10px]">DMARC Policy</span>
                      <p className="font-bold text-amber-400 flex items-center justify-center gap-1">
                        <AlertTriangle className="w-3.5 h-3.5" /> NONE
                      </p>
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
                    <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Recommended Defense Steps</h4>
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
                <span>BEC Defense Guidelines</span>
              </h3>
              <ul className="space-y-2.5 text-xs text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Lookalike Domains:</strong> Scammers register domains like <code>company-corp.xyz</code> to impersonate <code>company.com</code>.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-sky-400 font-bold">•</span>
                  <span><strong>Out-of-Band Verification:</strong> Always call executive senders on verified internal phone numbers before initiating wire transfers.</span>
                </li>
              </ul>
            </Card>
          </FadeIn>
        </div>
      </div>
    </PageTransition>
  );
};
