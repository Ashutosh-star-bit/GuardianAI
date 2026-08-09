import React, { useState } from 'react';
import { 
  ShieldAlert, 
  TrendingUp, 
  Globe, 
  CreditCard, 
  Mail, 
  Mic, 
  Laptop, 
  MapPin, 
  AlertTriangle, 
  ExternalLink,
  Flame,
  BarChart3
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';

export function ThreatIntelDashboardPage() {
  const [selectedChannel, setSelectedChannel] = useState<'ALL' | 'URL' | 'UPI' | 'EMAIL' | 'VOICE'>('ALL');

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-red-400">
            <ShieldAlert className="w-8 h-8 text-red-400" />
            Threat Intelligence & IOC Operations Center
          </h1>
          <p className="text-slate-400 mt-1">
            Real-time cyber threat feed tracking dangerous URLs, high-risk domains, UPI fraud handles, voice deepfakes, and browser extension stats.
          </p>
        </div>

        {/* Channel Filter Pills */}
        <div className="flex gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
          {(['ALL', 'URL', 'UPI', 'EMAIL', 'VOICE'] as const).map(ch => (
            <button
              key={ch}
              onClick={() => setSelectedChannel(ch)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                selectedChannel === ch 
                  ? 'bg-red-500 text-slate-950 shadow-sm' 
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {ch}
            </button>
          ))}
        </div>
      </div>

      {/* Top 4 Real-Time Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Active Blocked IOCs</span>
            <Flame className="w-5 h-5 text-red-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">14,280</div>
          <div className="text-[11px] text-red-400 mt-1 font-semibold">+412 added today</div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">High Risk Domains</span>
            <Globe className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">1,842</div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">Newly registered &lt; 7 days</div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Extension Installs</span>
            <Laptop className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">128,400</div>
          <div className="text-[11px] text-emerald-400 mt-1 font-semibold">Client Edge Protection</div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Voice Deepfake Calls</span>
            <Mic className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">342</div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">Voice AI clones intercepted</div>
        </Card>
      </div>

      {/* Grid: Dangerous URLs & High Risk Domains */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Most Dangerous URLs Table */}
        <Card className="p-6 bg-slate-800/60 border-slate-700/60">
          <h2 className="text-base font-bold text-slate-100 mb-4 flex items-center justify-between">
            <span className="flex items-center gap-2 text-red-400">
              <Globe className="w-5 h-5" />
              Most Dangerous Phishing URLs
            </span>
            <Badge variant="dangerous">CRITICAL</Badge>
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-2.5">Phishing URL</th>
                  <th className="p-2.5">Risk Score</th>
                  <th className="p-2.5">Reports</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 font-mono">
                {[
                  { url: "http://hdfc-kyc-update.top/login", score: 98, count: 142 },
                  { url: "http://cbi-police-verify.site/arrest", score: 96, count: 98 },
                  { url: "http://telegram-earn-tasks.biz/pay", score: 92, count: 74 },
                  { url: "http://sbi-netbank-renew.info/otp", score: 90, count: 52 }
                ].map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="p-2.5 text-red-400 font-semibold">{item.url}</td>
                    <td className="p-2.5 text-rose-400 font-bold">{item.score}/100</td>
                    <td className="p-2.5 text-slate-300">{item.count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Flagged UPI Fraud VPAs Table */}
        <Card className="p-6 bg-slate-800/60 border-slate-700/60">
          <h2 className="text-base font-bold text-slate-100 mb-4 flex items-center justify-between">
            <span className="flex items-center gap-2 text-amber-400">
              <CreditCard className="w-5 h-5" />
              Flagged Fraudulent UPI Handles
            </span>
            <Badge variant="caution">HIGH RISK</Badge>
          </h2>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-2.5">UPI VPA Handle</th>
                  <th className="p-2.5">Scam Vector</th>
                  <th className="p-2.5">Volume</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 font-mono">
                {[
                  { vpa: "cbi.police.dept@paytm", vector: "DIGITAL_ARREST", vol: "₹4.8L" },
                  { vpa: "hdfc.kyc.refund@ybl", vector: "BANKING_FRAUD", vol: "₹2.2L" },
                  { vpa: "parttime.jobs.bonus@okaxis", vector: "JOB_SCAM", vol: "₹1.5L" },
                  { vpa: "customs.clearance@icici", vector: "GIFT_SCAM", vol: "₹95k" }
                ].map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    <td className="p-2.5 text-amber-400 font-semibold">{item.vpa}</td>
                    <td className="p-2.5 text-cyan-400">{item.vector}</td>
                    <td className="p-2.5 text-slate-200">{item.vol}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {/* Grid: Email & Voice Scams + Geographic Regional Map Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Email Scams */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <h3 className="text-sm font-bold text-slate-100 mb-3 flex items-center gap-2 text-indigo-400">
            <Mail className="w-4 h-4" />
            Email Phishing Domains
          </h3>
          <ul className="space-y-2 text-xs font-mono text-slate-300">
            <li className="p-2 bg-slate-900 rounded-lg flex justify-between border border-slate-800">
              <span className="text-rose-400">alert@hdfc-notice.org</span>
              <span className="text-slate-500">DKIM FAIL</span>
            </li>
            <li className="p-2 bg-slate-900 rounded-lg flex justify-between border border-slate-800">
              <span className="text-rose-400">notice@cbi-gov.top</span>
              <span className="text-slate-500">SPF FAIL</span>
            </li>
          </ul>
        </Card>

        {/* Voice Scams */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <h3 className="text-sm font-bold text-slate-100 mb-3 flex items-center gap-2 text-cyan-400">
            <Mic className="w-4 h-4" />
            Voice Deepfake Caller Numbers
          </h3>
          <ul className="space-y-2 text-xs font-mono text-slate-300">
            <li className="p-2 bg-slate-900 rounded-lg flex justify-between border border-slate-800">
              <span className="text-cyan-400">+91 98765 43210</span>
              <span className="text-amber-400">CBI Voice Clone</span>
            </li>
            <li className="p-2 bg-slate-900 rounded-lg flex justify-between border border-slate-800">
              <span className="text-cyan-400">+91 87654 32109</span>
              <span className="text-amber-400">Customs Impersonator</span>
            </li>
          </ul>
        </Card>

        {/* Geographic Placeholder */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-100 mb-2 flex items-center gap-2 text-emerald-400">
              <MapPin className="w-4 h-4" />
              Regional Threat Distribution
            </h3>
            <p className="text-xs text-slate-400 mb-4">Top scam volume hotspots across national urban hubs.</p>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center">
              <span className="text-slate-300 font-medium">Delhi NCR</span>
              <div className="w-32 bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div className="bg-red-500 h-full w-[85%]" />
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-300 font-medium">Mumbai Metro</span>
              <div className="w-32 bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div className="bg-amber-500 h-full w-[65%]" />
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-300 font-medium">Bengaluru Tech Hub</span>
              <div className="w-32 bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div className="bg-cyan-500 h-full w-[45%]" />
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
export default ThreatIntelDashboardPage;
