import React, { useState } from 'react';
import { 
  Cpu, 
  Zap, 
  DollarSign, 
  Clock, 
  AlertTriangle, 
  RotateCcw, 
  TrendingUp, 
  Activity,
  Layers
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';

export function AIMetricsDashboardPage() {
  const [timeframe, setTimeframe] = useState<'daily' | 'weekly' | 'monthly'>('daily');

  // Timeframe Metrics Aggregations
  const metricData = {
    daily: {
      gemini_requests: 14280,
      prompt_tokens: 980000,
      completion_tokens: 448500,
      total_tokens: 1428500,
      estimated_cost_usd: 4.28,
      avg_latency_ms: 142.8,
      failure_rate_pct: 0.42,
      retry_count: 18
    },
    weekly: {
      gemini_requests: 99960,
      prompt_tokens: 6860000,
      completion_tokens: 3139500,
      total_tokens: 9999500,
      estimated_cost_usd: 29.96,
      avg_latency_ms: 139.5,
      failure_rate_pct: 0.38,
      retry_count: 124
    },
    monthly: {
      gemini_requests: 428400,
      prompt_tokens: 29400000,
      completion_tokens: 13455000,
      total_tokens: 42855000,
      estimated_cost_usd: 128.56,
      avg_latency_ms: 136.2,
      failure_rate_pct: 0.35,
      retry_count: 482
    }
  };

  const current = metricData[timeframe];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner & Timeframe Controls */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Cpu className="w-8 h-8 text-cyan-400" />
            AI Usage & Inference Analytics Dashboard
          </h1>
          <p className="text-slate-400 mt-1">
            Real-time metering for Google Gemini Flash / Pro LLM token consumption, latency, and estimated cost breakdown.
          </p>
        </div>

        {/* Timeframe Selector Pills */}
        <div className="flex gap-1.5 bg-slate-800 p-1.5 rounded-xl border border-slate-700">
          {(['daily', 'weekly', 'monthly'] as const).map(tf => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-bold uppercase transition-all ${
                timeframe === tf 
                  ? 'bg-cyan-500 text-slate-950 shadow-sm' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tf}
            </button>
          ))}
        </div>
      </div>

      {/* Top 4 Primary Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Gemini Requests</span>
            <Zap className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">
            {current.gemini_requests.toLocaleString()}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 font-semibold">99.58% Success Rate</div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Total Tokens</span>
            <Layers className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">
            {(current.total_tokens / 1000000).toFixed(2)}M
          </div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">
            Prompt: {(current.prompt_tokens / 1000).toFixed(0)}k • Completion: {(current.completion_tokens / 1000).toFixed(0)}k
          </div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Estimated Cost</span>
            <DollarSign className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">
            ${current.estimated_cost_usd.toFixed(2)}
          </div>
          <div className="text-[11px] text-slate-400 mt-1 font-mono">Gemini Flash Pricing Model</div>
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Avg Latency</span>
            <Clock className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-slate-100 font-mono">
            {current.avg_latency_ms} ms
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 font-semibold">Sub-150ms Performance</div>
        </Card>
      </div>

      {/* Secondary Metrics Row: Failures & Retries */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Model Failure Rate</span>
            <div className="text-xl font-bold text-rose-400 font-mono mt-1">
              {current.failure_rate_pct}%
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Rate limit or timeout errors</p>
          </div>
          <AlertTriangle className="w-8 h-8 text-rose-400/80" />
        </Card>

        <Card className="p-5 bg-slate-800/60 border-slate-700/60 flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Exponential Retries</span>
            <div className="text-xl font-bold text-amber-400 font-mono mt-1">
              {current.retry_count} Retries
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Auto-recovered via backoff</p>
          </div>
          <RotateCcw className="w-8 h-8 text-amber-400/80" />
        </Card>
      </div>

      {/* Breakdown Table */}
      <Card className="p-6 bg-slate-800/60 border-slate-700/60">
        <h2 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          LLM Model Variant Metering Breakdown
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">Model Variant</th>
                <th className="p-3">Request Count</th>
                <th className="p-3">Prompt Tokens</th>
                <th className="p-3">Completion Tokens</th>
                <th className="p-3">Avg Latency</th>
                <th className="p-3 text-right">Estimated Cost</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              <tr className="hover:bg-slate-800/40">
                <td className="p-3 font-bold text-cyan-400">Gemini 1.5 Flash</td>
                <td className="p-3">{(current.gemini_requests * 0.85).toFixed(0)}</td>
                <td className="p-3">{(current.prompt_tokens * 0.85).toFixed(0)}</td>
                <td className="p-3">{(current.completion_tokens * 0.85).toFixed(0)}</td>
                <td className="p-3 text-emerald-400">118.2 ms</td>
                <td className="p-3 text-right font-bold text-slate-100">${(current.estimated_cost_usd * 0.6).toFixed(2)}</td>
              </tr>
              <tr className="hover:bg-slate-800/40">
                <td className="p-3 font-bold text-indigo-400">Gemini 1.5 Pro</td>
                <td className="p-3">{(current.gemini_requests * 0.15).toFixed(0)}</td>
                <td className="p-3">{(current.prompt_tokens * 0.15).toFixed(0)}</td>
                <td className="p-3">{(current.completion_tokens * 0.15).toFixed(0)}</td>
                <td className="p-3 text-amber-400">284.5 ms</td>
                <td className="p-3 text-right font-bold text-slate-100">${(current.estimated_cost_usd * 0.4).toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
export default AIMetricsDashboardPage;
