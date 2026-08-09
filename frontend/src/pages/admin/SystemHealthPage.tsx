import React, { useState } from 'react';
import { 
  Activity, 
  Cpu, 
  HardDrive, 
  Database, 
  Server, 
  Brain, 
  FileText, 
  Mic, 
  Laptop, 
  Layers, 
  RefreshCw,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';

export function SystemHealthPage() {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 600);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-emerald-400">
            <Activity className="w-8 h-8 text-emerald-400" />
            Infrastructure & System Health Control Center
          </h1>
          <p className="text-slate-400 mt-1">
            Real-time telemetry monitoring server CPU, RAM, PostgreSQL pool, AI LLM services, OCR, Voice, and Task Queues.
          </p>
        </div>

        <button 
          onClick={handleRefresh}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 rounded-xl text-xs font-bold transition-all"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-emerald-400' : ''}`} />
          Refresh Health Status
        </button>
      </div>

      {/* Primary Server Hardware Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* CPU */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-cyan-400" /> CPU Utilization
            </span>
            <Badge variant="safe">14.2%</Badge>
          </div>
          <div className="w-full bg-slate-900 rounded-full h-2.5 overflow-hidden border border-slate-800">
            <div className="bg-cyan-400 h-full w-[14.2%]" />
          </div>
          <p className="text-[11px] text-slate-400 font-mono">8 Cores Active • 2.4 GHz</p>
        </Card>

        {/* RAM */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1.5">
              <HardDrive className="w-4 h-4 text-amber-400" /> RAM Memory
            </span>
            <Badge variant="safe">38.5%</Badge>
          </div>
          <div className="w-full bg-slate-900 rounded-full h-2.5 overflow-hidden border border-slate-800">
            <div className="bg-amber-400 h-full w-[38.5%]" />
          </div>
          <p className="text-[11px] text-slate-400 font-mono">6.16 GB / 16.0 GB Used</p>
        </Card>

        {/* Database */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1.5">
              <Database className="w-4 h-4 text-indigo-400" /> PostgreSQL Pool
            </span>
            <Badge variant="safe">HEALTHY</Badge>
          </div>
          <div className="text-xl font-bold font-mono text-slate-100">18 / 50 Active</div>
          <p className="text-[11px] text-slate-400 font-mono">Query Latency: 1.4 ms</p>
        </Card>

        {/* API Gateway */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-slate-400 uppercase flex items-center gap-1.5">
              <Server className="w-4 h-4 text-emerald-400" /> API Gateway
            </span>
            <Badge variant="safe">200 OK</Badge>
          </div>
          <div className="text-xl font-bold font-mono text-slate-100">38.4 req/sec</div>
          <p className="text-[11px] text-emerald-400 font-mono">99.98% Uptime</p>
        </Card>
      </div>

      {/* Subsystem Health Grid */}
      <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 pt-2">
        <Layers className="w-5 h-5 text-emerald-400" />
        Microservice & Processor Subsystem Status
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* AI LLM Service */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-cyan-400" />
              <span className="font-bold text-slate-100 text-sm">AI LLM Engine</span>
            </div>
            <Badge variant="safe">OPERATIONAL</Badge>
          </div>
          <p className="text-xs text-slate-400">Google Gemini Flash / Pro Inference API Gateway.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>Avg Latency: 142ms</span>
            <span className="text-emerald-400">100% Quota</span>
          </div>
        </Card>

        {/* OCR Service */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <FileText className="w-5 h-5 text-amber-400" />
              <span className="font-bold text-slate-100 text-sm">OCR Processor</span>
            </div>
            <Badge variant="safe">OPERATIONAL</Badge>
          </div>
          <p className="text-xs text-slate-400">Document layout analysis & Tesseract OCR worker pool.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>Workers: 4 Active</span>
            <span className="text-emerald-400">Queue: 0</span>
          </div>
        </Card>

        {/* Voice Service */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Mic className="w-5 h-5 text-indigo-400" />
              <span className="font-bold text-slate-100 text-sm">Voice Intelligence</span>
            </div>
            <Badge variant="safe">OPERATIONAL</Badge>
          </div>
          <p className="text-xs text-slate-400">Multi-threaded audio preprocessing & STT transcript cleaner.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>LRU Cache: 98% Hit</span>
            <span className="text-emerald-400">Memory Clean</span>
          </div>
        </Card>

        {/* Browser Extension Client Edge */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Laptop className="w-5 h-5 text-emerald-400" />
              <span className="font-bold text-slate-100 text-sm">Browser Extension</span>
            </div>
            <Badge variant="safe">ACTIVE</Badge>
          </div>
          <p className="text-xs text-slate-400">Client-side edge PII scrubbing & zero-knowledge scanning.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>Active Installs: 128.4k</span>
            <span className="text-emerald-400">Edge PII Scrub ON</span>
          </div>
        </Card>

        {/* Task Queues */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-purple-400" />
              <span className="font-bold text-slate-100 text-sm">Redis Task Queues</span>
            </div>
            <Badge variant="safe">OPTIMAL</Badge>
          </div>
          <p className="text-xs text-slate-400">Asynchronous Celery / Redis background worker queue.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>Pending Tasks: 0</span>
            <span className="text-emerald-400">Processed: 48.2k</span>
          </div>
        </Card>

        {/* Background Services */}
        <Card className="p-5 bg-slate-800/60 border-slate-700/60 space-y-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-teal-400" />
              <span className="font-bold text-slate-100 text-sm">Background Services</span>
            </div>
            <Badge variant="safe">HEALTHY</Badge>
          </div>
          <p className="text-xs text-slate-400">Scheduled analytics recorder & database backup tasks.</p>
          <div className="text-xs font-mono text-slate-300 pt-2 border-t border-slate-800/80 flex justify-between">
            <span>Cron Tasks: Active</span>
            <span className="text-emerald-400">Errors: 0</span>
          </div>
        </Card>
      </div>
    </div>
  );
}
export default SystemHealthPage;
