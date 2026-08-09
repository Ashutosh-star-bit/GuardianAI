import React from 'react';
import { motion } from 'framer-motion';

/**
 * GuardianAI Animated Threat Score Risk Gauge Component
 * Purpose: Provides a smooth 60 FPS animated progress bar arc and score index counter.
 */

export interface AnimatedRiskGaugeProps {
  score: number; // 0 to 100
  riskBand: 'safe' | 'caution' | 'dangerous';
  size?: 'sm' | 'md' | 'lg';
}

export const AnimatedRiskGauge: React.FC<AnimatedRiskGaugeProps> = ({
  score,
  riskBand,
  size = 'md',
}) => {
  const getGradient = () => {
    if (riskBand === 'dangerous') return 'from-amber-500 to-red-500';
    if (riskBand === 'caution') return 'from-sky-500 to-amber-500';
    return 'from-emerald-500 to-teal-400';
  };

  const getTextColor = () => {
    if (riskBand === 'dangerous') return 'text-red-400';
    if (riskBand === 'caution') return 'text-amber-400';
    return 'text-emerald-400';
  };

  return (
    <div className="space-y-2 text-center w-full">
      <div className="relative flex items-center justify-center">
        <motion.span
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className={`text-5xl font-black ${getTextColor()} tracking-tight`}
        >
          {score}
        </motion.span>
        <span className="text-sm font-bold text-slate-500 ml-1">/100</span>
      </div>

      {/* Progress Arc Bar */}
      <div className="w-full bg-slate-900 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${score}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className={`h-full bg-gradient-to-r ${getGradient()} rounded-full shadow-md`}
        />
      </div>
    </div>
  );
};
