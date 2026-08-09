import React from 'react';
import { ShieldCheck, Lock, Eye, Sparkles } from 'lucide-react';

export const FloatingShield3D: React.FC = () => {
  return (
    <div className="relative w-full max-w-md mx-auto aspect-square flex items-center justify-center perspective-1200 py-6 select-none">
      {/* 3D Background Glowing Ambient Sphere */}
      <div className="absolute w-64 h-64 bg-gradient-to-tr from-sky-500/20 via-purple-500/20 to-blue-600/30 rounded-full blur-3xl animate-pulse" />

      {/* 3D Outer Levitating Ring */}
      <div
        className="absolute w-80 h-80 rounded-full border border-sky-500/30 border-t-sky-400 animate-spin"
        style={{ animationDuration: '16s', transform: 'rotateX(65deg) rotateY(15deg)', transformStyle: 'preserve-3d' }}
      />

      {/* 3D Inner Opposite Orbit Ring */}
      <div
        className="absolute w-64 h-64 rounded-full border border-purple-500/30 border-b-purple-400 animate-spin"
        style={{ animationDuration: '10s', animationDirection: 'reverse', transform: 'rotateX(-65deg) rotateY(-15deg)', transformStyle: 'preserve-3d' }}
      />

      {/* Main 3D Cyber Shield Glass Card Stack */}
      <div
        className="relative z-10 w-64 h-80 rounded-3xl bg-gradient-to-b from-slate-900/95 via-slate-900/80 to-slate-950/95 border border-sky-500/40 p-6 shadow-[0_25px_60px_rgba(56,189,248,0.25)] backdrop-blur-2xl animate-float-3d flex flex-col items-center justify-between preserve-3d"
      >
        {/* Holographic Header Bar */}
        <div className="w-full flex items-center justify-between border-b border-slate-800 pb-3" style={{ transform: 'translateZ(25px)' }}>
          <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-sky-400">
            <Sparkles className="w-4 h-4 text-sky-400 animate-spin" style={{ animationDuration: '6s' }} />
            <span>GUARDIAN-AI v1.0</span>
          </div>
          <span className="text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full">
            ENCRYPTED
          </span>
        </div>

        {/* 3D Central Emblem */}
        <div className="relative py-4 flex flex-col items-center" style={{ transform: 'translateZ(45px)' }}>
          <div className="relative bg-gradient-to-b from-sky-500/20 to-blue-600/30 p-5 rounded-3xl border border-sky-400/50 shadow-[0_0_30px_rgba(56,189,248,0.4)]">
            <ShieldCheck className="w-16 h-16 text-sky-300 drop-shadow-[0_0_15px_#38bdf8]" />
            <div className="absolute -bottom-2 -right-2 bg-purple-600 p-2 rounded-xl border border-purple-300 shadow-lg">
              <Lock className="w-4 h-4 text-white" />
            </div>
          </div>
        </div>

        {/* Floating Stat Badges */}
        <div className="w-full grid grid-cols-2 gap-2 pt-2" style={{ transform: 'translateZ(30px)' }}>
          <div className="bg-slate-950/90 border border-slate-800 p-2 rounded-xl text-center">
            <div className="text-[10px] font-bold text-slate-400 uppercase">Detection</div>
            <div className="text-sm font-black text-sky-400 font-mono">99.8%</div>
          </div>
          <div className="bg-slate-950/90 border border-slate-800 p-2 rounded-xl text-center">
            <div className="text-[10px] font-bold text-slate-400 uppercase">Privacy</div>
            <div className="text-sm font-black text-emerald-400 font-mono">100% ZKP</div>
          </div>
        </div>
      </div>
    </div>
  );
};
