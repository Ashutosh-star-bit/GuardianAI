import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle } from 'lucide-react';

interface CinematicThreatGauge3DProps {
  score: number; // 0 to 100
  riskBand: 'safe' | 'caution' | 'dangerous';
}

export const CinematicThreatGauge3D: React.FC<CinematicThreatGauge3DProps> = ({ score, riskBand }) => {
  const getTheme = () => {
    switch (riskBand) {
      case 'dangerous':
        return {
          color: '#ef4444',
          glow: 'rgba(239,68,68,0.4)',
          textClass: 'text-red-400',
          borderClass: 'border-red-500/50',
          bgClass: 'bg-red-950/40',
          icon: ShieldAlert,
          label: 'HIGH THREAT SCAM DETECTED',
        };
      case 'caution':
        return {
          color: '#f59e0b',
          glow: 'rgba(245,158,11,0.4)',
          textClass: 'text-amber-400',
          borderClass: 'border-amber-500/50',
          bgClass: 'bg-amber-950/40',
          icon: AlertTriangle,
          label: 'SUSPICIOUS CAUTION WARNING',
        };
      default:
        return {
          color: '#10b981',
          glow: 'rgba(16,185,129,0.4)',
          textClass: 'text-emerald-400',
          borderClass: 'border-emerald-500/50',
          bgClass: 'bg-emerald-950/40',
          icon: ShieldCheck,
          label: 'CLEAN SAFE PAYLOAD',
        };
    }
  };

  const theme = getTheme();
  const IconComp = theme.icon;

  const circumference = 2 * Math.PI * 54;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="relative w-full max-w-xs mx-auto aspect-square flex flex-col items-center justify-center perspective-1000 my-4 select-none">
      {/* 3D Outer Glowing Aura Ring */}
      <div
        className="absolute w-60 h-60 rounded-full border border-slate-800 animate-spin"
        style={{
          animationDuration: '20s',
          transform: 'rotateX(45deg) rotateY(15deg)',
          boxShadow: `0 0 40px ${theme.glow}`,
          transformStyle: 'preserve-3d',
        }}
      />

      {/* SVG 3D Animated Circular Gauge Arc */}
      <div
        className="relative z-10 w-48 h-48 flex items-center justify-center preserve-3d animate-float-3d"
      >
        <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 120 120">
          {/* Background Track */}
          <circle
            cx="60"
            cy="60"
            r="54"
            className="text-slate-900"
            strokeWidth="8"
            stroke="currentColor"
            fill="transparent"
          />

          {/* Animated Risk Arc */}
          <circle
            cx="60"
            cy="60"
            r="54"
            stroke={theme.color}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
            style={{ filter: `drop-shadow(0 0 12px ${theme.color})` }}
          />
        </svg>

        {/* Center 3D Score Counter Shield */}
        <div
          className={`absolute inset-4 rounded-full ${theme.bgClass} border ${theme.borderClass} backdrop-blur-xl flex flex-col items-center justify-center gap-1 shadow-2xl preserve-3d`}
        >
          <IconComp className={`w-8 h-8 ${theme.textClass} animate-pulse`} />
          <div className="text-3xl font-black font-mono text-white tracking-tighter">
            {score}
            <span className="text-xs font-normal text-slate-400">/100</span>
          </div>
          <span className={`text-[9px] font-mono font-black uppercase tracking-wider ${theme.textClass}`}>
            {riskBand}
          </span>
        </div>
      </div>

      <div className={`mt-3 text-xs font-mono font-bold uppercase tracking-wider ${theme.textClass} text-center`}>
        {theme.label}
      </div>
    </div>
  );
};
