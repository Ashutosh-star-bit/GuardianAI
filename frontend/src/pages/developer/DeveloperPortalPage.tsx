import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Code, 
  KeyRound, 
  Webhook, 
  Copy, 
  Check, 
  Plus, 
  Activity, 
  ExternalLink,
  Terminal,
  Download,
  ListFilter,
  CreditCard,
  LifeBuoy,
  BookOpen,
  Home,
  Zap,
  ShieldCheck,
  Server
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';

export interface DeveloperKey {
  id: string;
  name: string;
  prefix: string;
  secret?: string;
  environment: 'LIVE' | 'TEST';
  tier: 'FREE' | 'PRO' | 'ENTERPRISE';
  rate_limit_rps: number;
  daily_quota: number;
  created_at: string;
}

export function DeveloperPortalPage() {
  const [activeTab, setActiveTab] = useState<
    'home' | 'api_keys' | 'usage' | 'playground' | 'docs' | 'pricing' | 'support' | 'examples'
  >('home');
  const [copiedKeyId, setCopiedKeyId] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<'curl' | 'python' | 'node' | 'go'>('curl');

  const [keys, setKeys] = useState<DeveloperKey[]>([
    {
      id: 'key_101',
      name: 'Mobile App Production Key',
      prefix: 'gai_live_88f9',
      secret: 'gai_live_88f92a110099xza21_prod',
      environment: 'LIVE',
      tier: 'PRO',
      rate_limit_rps: 100,
      daily_quota: 50000,
      created_at: '2026-08-01'
    },
    {
      id: 'key_102',
      name: 'Local Testing Sandbox',
      prefix: 'gai_test_44e1',
      secret: 'gai_test_44e11b882200abc12_test',
      environment: 'TEST',
      tier: 'FREE',
      rate_limit_rps: 10,
      daily_quota: 1000,
      created_at: '2026-08-01'
    }
  ]);

  const handleCopySecret = (keyId: string, secret?: string) => {
    if (!secret) return;
    navigator.clipboard.writeText(secret);
    setCopiedKeyId(keyId);
    setTimeout(() => setCopiedKeyId(null), 2000);
  };

  const handleGenerateKey = () => {
    const newKey: DeveloperKey = {
      id: `key_${Date.now().toString().slice(-4)}`,
      name: 'New Integration Key',
      prefix: 'gai_live_99a8',
      secret: `gai_live_99a8${Math.random().toString(36).slice(2)}`,
      environment: 'LIVE',
      tier: 'PRO',
      rate_limit_rps: 100,
      daily_quota: 50000,
      created_at: new Date().toISOString().split('T')[0]
    };
    setKeys([newKey, ...keys]);
  };

  const handleRevokeKey = (id: string) => {
    setKeys(keys.filter(k => k.id !== id));
  };

  const codeSnippets = {
    curl: `curl -X POST "https://api.guardianai.io/api/v1/scan/url" \\
  -H "Authorization: Bearer gai_live_88f92a110099xza21_prod" \\
  -H "Content-Type: application/json" \\
  -d '{"target_url": "http://hdfc-verify.top"}'`,
    python: `from guardianai import GuardianAIClient

client = GuardianAIClient(api_key="gai_live_88f92a110099xza21_prod")
result = client.scan_url("http://hdfc-verify.top")
print(f"Risk Score: {result.threat_score}")`,
    node: `const { GuardianAIClient } = require('@guardianai/sdk');
const client = new GuardianAIClient({ apiKey: 'gai_live_88f92a110099xza21_prod' });
const res = await client.scanUrl('http://hdfc-verify.top');
console.log(res);`,
    go: `package main
import (
    "fmt"
    "github.com/guardianai/sdk-go"
)
func main() {
    client := guardianai.NewClient("gai_live_88f92a110099xza21_prod")
    res, _ := client.ScanURL("http://hdfc-verify.top")
    fmt.Println(res.ThreatScore)
}`
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Code className="w-8 h-8 text-cyan-400" />
            GuardianAI Developer Portal & API Gateway
          </h1>
          <p className="text-slate-400 mt-1">
            Build, test, and deploy explainable anti-scam AI protections using our polyglot REST APIs & SDKs.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/developer/playground"
            className="flex items-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-bold rounded-lg border border-slate-700 transition-all"
          >
            <Terminal className="w-3.5 h-3.5" /> Launch Playground
          </Link>
          <Button variant="primary" onClick={handleGenerateKey} className="flex items-center gap-2 text-xs font-bold">
            <Plus className="w-4 h-4" /> Generate API Key
          </Button>
        </div>
      </div>

      {/* Primary Developer SLA Quotas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <span className="text-xs font-semibold text-slate-400 uppercase">Current Subscription Tier</span>
          <div className="text-2xl font-black text-cyan-400 mt-1 font-mono">PRO BUSINESS</div>
          <p className="text-xs text-slate-400 mt-1">100 RPS Sliding Window Rate Limit</p>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <span className="text-xs font-semibold text-slate-400 uppercase">Daily API Quota Usage</span>
          <div className="text-2xl font-black text-emerald-400 mt-1 font-mono">14,280 / 50,000</div>
          <p className="text-xs text-slate-400 mt-1">Resetting in 18 hours (28.5% used)</p>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <span className="text-xs font-semibold text-slate-400 uppercase">Average Latency SLA</span>
          <div className="text-2xl font-black text-amber-400 mt-1 font-mono">142.5 ms</div>
          <p className="text-xs text-emerald-400 mt-1">99.98% Uptime SLA Guarantee</p>
        </Card>
      </div>

      {/* Portal Tabs Navigation */}
      <div className="flex overflow-x-auto border-b border-slate-800 space-x-6 pb-1">
        {[
          { key: 'home', label: 'Overview', icon: Home },
          { key: 'api_keys', label: 'API Keys', icon: KeyRound },
          { key: 'usage', label: 'Usage Telemetry', icon: Activity },
          { key: 'playground', label: 'API Playground', icon: Terminal },
          { key: 'docs', label: 'Documentation', icon: BookOpen },
          { key: 'pricing', label: 'Pricing Plans', icon: CreditCard },
          { key: 'examples', label: 'Code Examples', icon: Code },
          { key: 'support', label: 'Support & SLA', icon: LifeBuoy }
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center gap-2 pb-3 text-sm font-semibold transition-colors border-b-2 whitespace-nowrap ${
                activeTab === tab.key
                  ? 'border-cyan-400 text-cyan-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB 1: OVERVIEW HOME */}
      {activeTab === 'home' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-6">
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Zap className="w-5 h-5 text-cyan-400" />
            Developer Getting Started Overview
          </h2>
          <p className="text-slate-300 text-sm leading-relaxed">
            Welcome to the GuardianAI Developer Hub. Protect your web apps, mobile apps, and enterprise backend pipelines against phishing URLs, smishing SMS, digital arrest fraud, and BEC wire fraud.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
              <h3 className="font-bold text-cyan-400 text-sm">1. Get API Credentials</h3>
              <p className="text-xs text-slate-400">Generate a live or sandbox key under the API Keys tab.</p>
            </div>
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
              <h3 className="font-bold text-cyan-400 text-sm">2. Install SDK</h3>
              <p className="text-xs text-slate-400">Install native bindings for Python, Node.js, Go, or Java.</p>
            </div>
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
              <h3 className="font-bold text-cyan-400 text-sm">3. Test in Playground</h3>
              <p className="text-xs text-slate-400">Execute interactive REST calls in our sandbox playground.</p>
            </div>
          </div>
        </Card>
      )}

      {/* TAB 2: API KEYS */}
      {activeTab === 'api_keys' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 mb-2">Active API Credentials</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300 font-mono">
              <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-3">Key Name</th>
                  <th className="p-3">Environment</th>
                  <th className="p-3">Prefix / Secret</th>
                  <th className="p-3">Rate Limit</th>
                  <th className="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {keys.map(k => (
                  <tr key={k.id} className="hover:bg-slate-800/40">
                    <td className="p-3 font-bold text-slate-100">{k.name}</td>
                    <td className="p-3">
                      <Badge variant={k.environment === 'LIVE' ? 'safe' : 'caution'}>{k.environment}</Badge>
                    </td>
                    <td className="p-3 text-cyan-400 flex items-center gap-2">
                      <span>{k.prefix}••••••••••••</span>
                      <button onClick={() => handleCopySecret(k.id, k.secret)} className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-cyan-400">
                        {copiedKeyId === k.id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>
                    </td>
                    <td className="p-3">{k.rate_limit_rps} RPS</td>
                    <td className="p-3 text-right">
                      <button onClick={() => handleRevokeKey(k.id)} className="px-2.5 py-1 bg-slate-800 text-rose-400 rounded text-[11px] font-bold">
                        Revoke
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* TAB 3: USAGE */}
      {activeTab === 'usage' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-cyan-400" />
              API Usage & Latency Telemetry
            </h2>
            <Link to="/developer/analytics" className="text-xs text-cyan-400 hover:underline font-bold flex items-center gap-1">
              View Detailed Analytics Console <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
          <p className="text-slate-400 text-xs">Total Requests: 142,850 • Avg Latency: 142.5ms • p95: 280ms • Bandwidth: 1.39 GB</p>
        </Card>
      )}

      {/* TAB 4: PLAYGROUND */}
      {activeTab === 'playground' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4 text-center">
          <Terminal className="w-12 h-12 text-cyan-400 mx-auto" />
          <h2 className="text-xl font-bold text-slate-100">Interactive REST API Playground</h2>
          <p className="text-slate-400 text-xs max-w-md mx-auto">
            Test live GuardianAI endpoints in real-time, edit request JSON payloads, and inspect HTTP response headers.
          </p>
          <Link
            to="/developer/playground"
            className="inline-block px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs rounded-xl transition-all"
          >
            Launch Full Interactive Playground
          </Link>
        </Card>
      )}

      {/* TAB 5: DOCS */}
      {activeTab === 'docs' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            OpenAPI 3.0 Documentation References
          </h2>
          <div className="flex gap-4">
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="p-4 bg-slate-900 border border-slate-800 rounded-xl hover:border-cyan-500 transition-all text-xs font-bold text-cyan-400 flex items-center gap-2">
              <ExternalLink className="w-4 h-4" /> Open Swagger UI (/docs)
            </a>
            <a href="http://localhost:8000/redoc" target="_blank" rel="noopener noreferrer" className="p-4 bg-slate-900 border border-slate-800 rounded-xl hover:border-cyan-500 transition-all text-xs font-bold text-purple-400 flex items-center gap-2">
              <ExternalLink className="w-4 h-4" /> Open ReDoc (/redoc)
            </a>
          </div>
        </Card>
      )}

      {/* TAB 6: PRICING */}
      {activeTab === 'pricing' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-emerald-400" />
            Developer Platform Tier Pricing
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
              <span className="font-bold text-slate-400">FREE SANDBOX</span>
              <div className="text-2xl font-black text-white">$0 / mo</div>
              <p className="text-slate-400">10 RPS • 1,000 req/day</p>
            </div>
            <div className="p-4 bg-slate-900 border border-cyan-500 rounded-xl space-y-2">
              <span className="font-bold text-cyan-400">PRO BUSINESS</span>
              <div className="text-2xl font-black text-cyan-400">$99 / mo</div>
              <p className="text-slate-400">100 RPS • 50,000 req/day</p>
            </div>
            <div className="p-4 bg-slate-900 border border-purple-500 rounded-xl space-y-2">
              <span className="font-bold text-purple-400">ENTERPRISE SLA</span>
              <div className="text-2xl font-black text-purple-400">Custom</div>
              <p className="text-slate-400">1,000 RPS • 20M req/day</p>
            </div>
          </div>
        </Card>
      )}

      {/* TAB 7: CODE EXAMPLES */}
      {activeTab === 'examples' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
              <Code className="w-5 h-5 text-cyan-400" />
              Polyglot Integration Code Generator
            </h2>
            <div className="flex gap-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
              {(['curl', 'python', 'node', 'go'] as const).map(lang => (
                <button
                  key={lang}
                  onClick={() => setSelectedLanguage(lang)}
                  className={`px-3 py-1 rounded text-xs font-bold uppercase transition-all ${
                    selectedLanguage === lang ? 'bg-cyan-500 text-slate-950' : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 overflow-x-auto">
            <pre>{codeSnippets[selectedLanguage]}</pre>
          </div>
        </Card>
      )}

      {/* TAB 8: SUPPORT */}
      {activeTab === 'support' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <LifeBuoy className="w-5 h-5 text-amber-400" />
            Developer Support & 99.98% Uptime SLA
          </h2>
          <p className="text-slate-300 text-sm">Need help integrating? Join our Discord developer community or file an Enterprise SLA ticket.</p>
        </Card>
      )}
    </div>
  );
}
export default DeveloperPortalPage;
