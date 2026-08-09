import React from 'react';
import { 
  BarChart3, 
  Activity, 
  Clock, 
  ShieldAlert, 
  Cpu, 
  HardDrive, 
  Users, 
  KeyRound,
  TrendingUp,
  Server
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { FadeIn } from '../../components/common/FadeIn';

export function APIAnalyticsPage() {
  const analytics = {
    total_requests: 142850,
    error_rate_pct: 0.15,
    avg_latency_ms: 142.5,
    p95_latency_ms: 280.0,
    p99_latency_ms: 450.0,
    total_tokens: 2465000,
    bandwidth_gb: 1.39,
    active_users: 1420,
    active_keys: 3840,
    top_endpoints: [
      { route: '/api/v1/scan/url', requests: 54200, pct: 38, avg_latency: '115 ms' },
      { route: '/api/v1/scan/text', requests: 48100, pct: 34, avg_latency: '142 ms' },
      { route: '/api/v1/threats/lookup', requests: 28400, pct: 20, avg_latency: '85 ms' },
      { route: '/api/v1/scan/ocr', requests: 12150, pct: 8, avg_latency: '320 ms' }
    ]
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <BarChart3 className="w-8 h-8 text-cyan-400" />
            Developer API Usage Telemetry & SLA Analytics
          </h1>
          <p className="text-slate-400 mt-1">
            Real-time API requests, latency percentiles (p50/p95/p99), token consumption, bandwidth, and top routes.
          </p>
        </div>
      </div>

      {/* Metric Cards Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <FadeIn delay={0.05}>
          <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-2">
            <div className="flex justify-between items-center text-slate-400 text-xs font-bold uppercase">
              <span>Total API Requests</span>
              <Activity className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-3xl font-black text-white font-mono">{analytics.total_requests.toLocaleString()}</div>
            <span className="text-xs font-bold text-emerald-400 flex items-center gap-1">
              <TrendingUp className="w-3.5 h-3.5" /> +18.4% this week
            </span>
          </Card>
        </FadeIn>

        <FadeIn delay={0.1}>
          <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-2">
            <div className="flex justify-between items-center text-slate-400 text-xs font-bold uppercase">
              <span>Average Latency SLA</span>
              <Clock className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-black text-amber-400 font-mono">{analytics.avg_latency_ms} ms</div>
            <p className="text-xs text-slate-400">p95: {analytics.p95_latency_ms}ms • p99: {analytics.p99_latency_ms}ms</p>
          </Card>
        </FadeIn>

        <FadeIn delay={0.15}>
          <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-2">
            <div className="flex justify-between items-center text-slate-400 text-xs font-bold uppercase">
              <span>Tokens & Bandwidth</span>
              <Cpu className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-3xl font-black text-purple-400 font-mono">2.46M Tokens</div>
            <p className="text-xs text-slate-400">{analytics.bandwidth_gb} GB Data Transferred</p>
          </Card>
        </FadeIn>

        <FadeIn delay={0.2}>
          <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-2">
            <div className="flex justify-between items-center text-slate-400 text-xs font-bold uppercase">
              <span>Active Developers & Keys</span>
              <Users className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl font-black text-emerald-400 font-mono">{analytics.active_keys.toLocaleString()} Keys</div>
            <p className="text-xs text-slate-400">{analytics.active_users.toLocaleString()} Active Developers</p>
          </Card>
        </FadeIn>
      </div>

      {/* Top Endpoints Table */}
      <FadeIn delay={0.25}>
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Server className="w-5 h-5 text-cyan-400" />
            Top API Endpoints Traffic Distribution
          </h2>

          <div className="space-y-4 pt-2">
            {analytics.top_endpoints.map((ep, idx) => (
              <div key={idx} className="space-y-1.5">
                <div className="flex justify-between text-xs font-bold font-mono">
                  <span className="text-cyan-400">{ep.route}</span>
                  <span className="text-slate-400">{ep.requests.toLocaleString()} req ({ep.pct}%) • Avg: {ep.avg_latency}</span>
                </div>
                <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden">
                  <div className="h-full bg-cyan-500 rounded-full" style={{ width: `${ep.pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </Card>
      </FadeIn>
    </div>
  );
}
export default APIAnalyticsPage;
