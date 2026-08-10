import React, { useState } from 'react';
import {
  FileText,
  ShieldAlert,
  Download,
  ExternalLink,
  Building2,
  PhoneCall,
  CheckCircle2,
  AlertTriangle,
  Send,
  FileCheck,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { ThreeDCard } from '../components/3d/ThreeDCard';

export const ReportsPage: React.FC = () => {
  const { scanHistory } = useAuth();
  const { showToast } = useToast();

  const dangerousReports = scanHistory.filter(
    (s) => s.riskBand === 'dangerous' || s.riskBand === 'caution'
  );

  const handleExportEvidence = (reportId: string) => {
    const report = scanHistory.find((s) => s.id === reportId);
    if (!report) return;

    const evidenceText = `
========================================================================
OFFICIAL CYBERCRIME THREAT EVIDENCE PACKET - GUARDIAN AI TELEMETRY
========================================================================
Report ID: ${report.id}
Date/Time of Incident: ${new Date(report.timestamp).toUTCString()}
Threat Classification: ${report.riskBand.toUpperCase()} (Threat Score: ${report.threatScore}/100)
Channel Vector: ${report.payloadType}

INCIDENT PAYLOAD EVIDENCE:
------------------------------------------------------------------------
${report.payloadSnippet}

AI EXPLAINABLE RATIONALE & ANOMALY ANALYSIS:
------------------------------------------------------------------------
${report.plainRationale}

RECOMMENDED ACTIONABLE STEPS:
------------------------------------------------------------------------
${report.remediation.map((r: string, i: number) => `${i + 1}. ${r}`).join('\n')}

========================================================================
Exported by GuardianAI Zero-Knowledge Protection System.
Submit this file to your local Law Enforcement or National Cybercrime Portal.
========================================================================
`;

    const blob = new Blob([evidenceText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Cybercrime_Evidence_${report.id}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('success', 'Evidence Packet Exported', 'Official evidence packet downloaded. Ready for government submission!');
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <FileText className="w-4 h-4" />
          <span>Fraud Incident Reporting & Compliance</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Fraud Incident Center</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Generate official evidence packets and report malicious scams to authorized government law enforcement agencies.
        </p>
      </div>

      {/* Official Government & Authorized Cybercrime Portals Guide */}
      <Card className="p-6 border-sky-500/30 bg-slate-900/90 space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
          <div className="p-2.5 bg-sky-500/10 border border-sky-500/30 rounded-xl text-sky-400">
            <Building2 className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-black text-white">Official Government Cybercrime Reporting Guide</h2>
            <p className="text-xs text-slate-400">
              Report verified scam messages, phishing links, BEC emails, or QR codes to official government authorities for legal action.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* US FTC / FBI */}
          <ThreeDCard glowColor="cyan">
            <div className="bg-slate-950/90 border border-sky-500/30 p-4 rounded-2xl space-y-3 backdrop-blur-xl h-full flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-black text-white">US FTC & FBI IC3</h3>
                  <span className="text-[10px] bg-sky-500/20 text-sky-300 px-2 py-0.5 rounded font-mono font-bold">UNITED STATES</span>
                </div>
                <p className="text-xs text-slate-400">
                  Federal Trade Commission (FTC) & FBI Internet Crime Complaint Center.
                </p>
              </div>
              <div className="space-y-1.5 text-xs font-bold">
                <a
                  href="https://reportfraud.ftc.gov"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between p-2 bg-slate-900 hover:bg-slate-800 text-sky-400 rounded-xl transition-all"
                >
                  <span>ReportFraud.ftc.gov</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
                <a
                  href="https://www.ic3.gov"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between p-2 bg-slate-900 hover:bg-slate-800 text-sky-400 rounded-xl transition-all"
                >
                  <span>FBI IC3 (ic3.gov)</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </ThreeDCard>

          {/* India Portal */}
          <ThreeDCard glowColor="amber">
            <div className="bg-slate-950/90 border border-amber-500/30 p-4 rounded-2xl space-y-3 backdrop-blur-xl h-full flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-black text-white">India Cyber Crime Portal</h3>
                  <span className="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded font-mono font-bold">INDIA</span>
                </div>
                <p className="text-xs text-slate-400">
                  National Cyber Crime Reporting Portal & Telecom Regulator (Sanchar Saathi / Chakshu).
                </p>
              </div>
              <div className="space-y-1.5 text-xs font-bold">
                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between p-2 bg-slate-900 hover:bg-slate-800 text-amber-400 rounded-xl transition-all"
                >
                  <span>cybercrime.gov.in</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
                <div className="flex items-center justify-between p-2 bg-slate-900 text-amber-300 rounded-xl">
                  <span>National Helpline: 1930</span>
                  <PhoneCall className="w-3.5 h-3.5 text-amber-400" />
                </div>
              </div>
            </div>
          </ThreeDCard>

          {/* UK & International */}
          <ThreeDCard glowColor="emerald">
            <div className="bg-slate-950/90 border border-emerald-500/30 p-4 rounded-2xl space-y-3 backdrop-blur-xl h-full flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-black text-white">UK & International</h3>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded font-mono font-bold">GLOBAL</span>
                </div>
                <p className="text-xs text-slate-400">
                  Action Fraud UK police agency & global CERT computer emergency response teams.
                </p>
              </div>
              <div className="space-y-1.5 text-xs font-bold">
                <a
                  href="https://www.actionfraud.police.uk"
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center justify-between p-2 bg-slate-900 hover:bg-slate-800 text-emerald-400 rounded-xl transition-all"
                >
                  <span>ActionFraud.police.uk</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </ThreeDCard>
        </div>
      </Card>

      {/* Real Flagged Fraud Threats List */}
      <div className="space-y-4">
        <h2 className="text-lg font-black text-white flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-red-400" />
          <span>Flagged Fraud Incidents ({dangerousReports.length})</span>
        </h2>

        {dangerousReports.length === 0 ? (
          <Card className="text-center py-10 border-slate-800 bg-slate-900/90 space-y-2">
            <p className="text-xs text-slate-400">
              No high-risk fraud incidents recorded yet. Run a threat scan to automatically flag threats!
            </p>
          </Card>
        ) : (
          <div className="space-y-3">
            {dangerousReports.map((item) => (
              <Card key={item.id} className="p-4 border-red-500/30 bg-slate-900/90 space-y-3">
                <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                  <div>
                    <div className="flex items-center gap-2 text-xs font-bold text-white mb-1">
                      <span className="px-2 py-0.5 bg-red-500/20 text-red-400 border border-red-500/40 rounded uppercase text-[10px]">
                        {item.riskBand}
                      </span>
                      <span>{item.payloadType} Incident</span>
                      <span className="text-slate-500 font-mono text-[10px]">
                        {new Date(item.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 font-mono line-clamp-1">{item.payloadSnippet}</p>
                  </div>

                  <Button
                    onClick={() => handleExportEvidence(item.id)}
                    className="bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-xs py-2 px-3 rounded-xl flex items-center gap-1.5 shrink-0"
                  >
                    <Download className="w-4 h-4" />
                    <span>Download Evidence Packet</span>
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </PageTransition>
  );
};
