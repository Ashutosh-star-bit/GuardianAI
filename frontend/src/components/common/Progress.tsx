import React from 'react';
import { motion } from 'framer-motion';

/**
 * GuardianAI Animated Progress Bar Component
 */

export interface ProgressProps {
  value: number; // 0 - 100
  max?: number;
  showLabel?: boolean;
  color?: 'emerald' | 'amber' | 'red' | 'sky';
  className?: string;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  max = 100,
  showLabel = false,
  color,
  className = '',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const getAutoColor = () => {
    if (color) {
      if (color === 'emerald') return 'bg-emerald-500';
      if (color === 'amber') return 'bg-amber-500';
      if (color === 'red') return 'bg-red-500';
      return 'bg-sky-500';
    }
    if (percentage <= 30) return 'bg-emerald-500';
    if (percentage <= 70) return 'bg-amber-500';
    return 'bg-red-500';
  };

  return (
    <div className={`space-y-1 w-full ${className}`}>
      {showLabel && (
        <div className="flex justify-between text-xs font-bold text-slate-300">
          <span>Progress</span>
          <span className="font-mono">{Math.round(percentage)}%</span>
        </div>
      )}
      <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden border border-slate-800 p-0.5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          className={`h-full rounded-full ${getAutoColor()}`}
        />
      </div>
    </div>
  );
};
