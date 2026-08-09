import React from 'react';
import { ShieldAlert, Globe, Radio } from 'lucide-react';

export const ThreatSphere3D: React.FC = () => {
  return (
    <div className="relative w-full aspect-square max-w-[200px] mx-auto flex items-center justify-center perspective-1000 my-2 select-none">
      {/* 3D Outer Orbiting Ring 1 */}
      <div
        className="absolute w-44 h-44 rounded-full border border-sky-500/30 border-t-sky-400 animate-spin"
        style={{ animationDuration: '12s', transform: 'rotateX(70deg) rotateY(20deg)', transformStyle: 'preserve-3d' }}
      />

      {/* 3D Outer Orbiting Ring 2 */}
      <div
        className="absolute w-36 h-36 rounded-full border border-red-500/40 border-b-red-400 animate-spin"
        style={{ animationDuration: '8s', animationDirection: 'reverse', transform: 'rotateX(-65deg) rotateY(-20deg)', transformStyle: 'preserve-3d' }}
      />

      {/* Center 3D Floating Threat Globe */}
      <div
        className="relative z-10 w-24 h-24 rounded-full bg-gradient-to-tr from-slate-950 via-slate-900 to-sky-950/80 border border-sky-500/50 flex flex-col items-center justify-center gap-1 shadow-[0_0_30px_rgba(56,189,248,0.3)] backdrop-blur-xl animate-float-3d preserve-3d"
      >
        <Globe className="w-8 h-8 text-sky-400 animate-pulse" />
        <span className="text-[9px] font-mono font-bold text-sky-300 uppercase tracking-widest">
          SENSORS ACTIVE
        </span>
      </div>

      {/* Orbiting Threat Blips */}
      <div className="absolute top-2 right-4 flex items-center gap-1 bg-red-950/90 border border-red-500/40 px-2 py-0.5 rounded-full text-[9px] font-bold text-red-300 shadow-md">
        <Radio className="w-2.5 h-2.5 text-red-400 animate-ping" />
        <span>SMS Phishing</span>
      </div>

      <div className="absolute bottom-2 left-4 flex items-center gap-1 bg-amber-950/90 border border-amber-500/40 px-2 py-0.5 rounded-full text-[9px] font-bold text-amber-300 shadow-md">
        <ShieldAlert className="w-2.5 h-2.5 text-amber-400" />
        <span>Digital Arrest</span>
      </div>
    </div>
  );
};
