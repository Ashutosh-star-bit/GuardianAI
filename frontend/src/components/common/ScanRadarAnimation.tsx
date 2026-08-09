import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Sparkles } from 'lucide-react';

/**
 * GuardianAI Scan Radar Pulse Animation Component
 * Purpose: Renders a sweeping radar beam and expanding pulse rings during AI threat inspection.
 */

export interface ScanRadarAnimationProps {
  label?: string;
}

export const ScanRadarAnimation: React.FC<ScanRadarAnimationProps> = ({
  label = 'AI Threat Radar Active...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4 text-center">
      <div className="relative w-28 h-28 flex items-center justify-center">
        {/* Expanding Pulse Ring 1 */}
        <motion.div
          animate={{ scale: [1, 1.8], opacity: [0.6, 0] }}
          transition={{ repeat: Infinity, duration: 1.8, ease: 'easeOut' }}
          className="absolute inset-0 rounded-full border-2 border-sky-400 bg-sky-500/10"
        />

        {/* Expanding Pulse Ring 2 */}
        <motion.div
          animate={{ scale: [1, 1.8], opacity: [0.6, 0] }}
          transition={{ repeat: Infinity, duration: 1.8, delay: 0.6, ease: 'easeOut' }}
          className="absolute inset-0 rounded-full border-2 border-blue-500 bg-blue-500/10"
        />

        {/* Center Shield Core */}
        <motion.div
          animate={{ scale: [0.95, 1.05, 0.95] }}
          transition={{ repeat: Infinity, duration: 1.5, ease: 'easeInOut' }}
          className="relative z-10 bg-slate-900 border-2 border-sky-400 p-4 rounded-2xl shadow-xl shadow-sky-500/20 text-sky-400"
        >
          <Shield className="w-10 h-10 animate-pulse" />
        </motion.div>
      </div>

      <div className="space-y-1">
        <p className="text-xs font-bold text-white tracking-wider uppercase flex items-center justify-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-sky-400 animate-spin" />
          <span>{label}</span>
        </p>
        <p className="text-[11px] text-slate-400 font-mono">Sweeping 14 Psychological Manipulative Signal Detectors</p>
      </div>
    </div>
  );
};
