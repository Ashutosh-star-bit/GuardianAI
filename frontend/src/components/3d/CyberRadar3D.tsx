import React from 'react';
import { ShieldCheck, Cpu, Radio, Zap } from 'lucide-react';

interface CyberRadar3DProps {
  isScanning?: boolean;
  statusText?: string;
}

export const CyberRadar3D: React.FC<CyberRadar3DProps> = ({
  isScanning = false,
  statusText = 'AI Neural Protection Active',
}) => {
  return (
    <div className="relative w-full max-w-sm mx-auto aspect-square flex items-center justify-center perspective-1000 my-4 select-none">
      {/* 3D Perspective Cyber Floor Grid */}
      <div className="absolute inset-0 rounded-full cyber-grid-3d opacity-30 pointer-events-none" />

      {/* Outer 3D Concentric Ring 1 */}
      <div
        className={`absolute w-72 h-72 rounded-full border border-sky-500/20 transition-all duration-700 ${
          isScanning ? 'border-sky-400/80 scale-105 shadow-[0_0_30px_rgba(56,189,248,0.3)]' : ''
        }`}
        style={{ transform: 'rotateX(55deg) rotateZ(0deg)', transformStyle: 'preserve-3d' }}
      >
        <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-sky-400 rounded-full shadow-[0_0_10px_#38bdf8]" />
      </div>

      {/* 3D Concentric Ring 2 */}
      <div
        className={`absolute w-56 h-56 rounded-full border border-dashed border-sky-400/30 transition-all duration-700 ${
          isScanning ? 'animate-spin border-sky-300 shadow-[0_0_20px_rgba(56,189,248,0.4)]' : ''
        }`}
        style={{ transform: 'rotateX(55deg) rotateZ(45deg)', transformStyle: 'preserve-3d' }}
      />

      {/* 3D Concentric Ring 3 */}
      <div
        className="absolute w-40 h-40 rounded-full border border-purple-500/30"
        style={{ transform: 'rotateX(55deg) rotateZ(-30deg)', transformStyle: 'preserve-3d' }}
      />

      {/* 3D Rotating Radar Sweep Line */}
      {isScanning && (
        <div
          className="absolute w-64 h-64 rounded-full border-r-2 border-sky-400 animate-radar-3d pointer-events-none"
          style={{
            transform: 'rotateX(55deg)',
            background: 'conic-gradient(from 0deg at 50% 50%, rgba(56,189,248,0.3) 0deg, transparent 60deg)',
          }}
        />
      )}

      {/* Center Stationary 3D Neural Core Sphere */}
      <div
        className={`relative z-10 w-24 h-24 rounded-3xl bg-slate-900/90 border border-sky-500/50 flex flex-col items-center justify-center gap-1 shadow-2xl backdrop-blur-xl ${
          isScanning ? 'border-sky-400 shadow-[0_0_35px_rgba(56,189,248,0.5)]' : 'shadow-[0_0_20px_rgba(56,189,248,0.2)]'
        }`}
        style={{ transformStyle: 'preserve-3d' }}
      >
        <div className="bg-sky-500/20 p-2.5 rounded-2xl border border-sky-400/40 relative">
          <Cpu className={`w-7 h-7 ${isScanning ? 'text-sky-300 animate-pulse' : 'text-sky-400'}`} />
          {isScanning && (
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
          )}
        </div>
        <span className="text-[10px] font-mono font-bold text-sky-300 tracking-wider uppercase">
          {isScanning ? 'SCANNING' : 'ONLINE'}
        </span>
      </div>

      {/* Floating Orbital Sensor Nodes */}
      <div className="absolute top-6 left-10 flex items-center gap-1 bg-slate-950/80 border border-slate-800 px-2 py-1 rounded-lg text-[10px] font-mono text-slate-300 shadow-lg">
        <Radio className="w-3 h-3 text-sky-400 animate-pulse" />
        <span>XAI BERT-v4</span>
      </div>

      <div className="absolute bottom-6 right-10 flex items-center gap-1 bg-slate-950/80 border border-slate-800 px-2 py-1 rounded-lg text-[10px] font-mono text-slate-300 shadow-lg">
        <Zap className="w-3 h-3 text-amber-400" />
        <span>0.1ms Latency</span>
      </div>
    </div>
  );
};
