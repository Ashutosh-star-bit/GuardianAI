import React from 'react';

/**
 * GuardianAI Risk & Status Badge Component
 */

export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'safe' | 'caution' | 'dangerous' | 'info' | 'neutral';
  size?: 'sm' | 'md';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  size = 'md',
  className = '',
}) => {
  const variantClasses = {
    safe: 'badge-risk-safe',
    caution: 'badge-risk-caution',
    dangerous: 'badge-risk-dangerous',
    info: 'bg-sky-950 text-sky-300 border border-sky-600/50 px-2.5 py-0.5 rounded-full font-bold text-xs',
    neutral: 'bg-slate-800 text-slate-300 border border-slate-700 px-2.5 py-0.5 rounded-full font-bold text-xs',
  };

  const sizeClasses = {
    sm: 'text-[10px] px-2 py-0.5',
    md: 'text-xs px-3 py-1',
  };

  return (
    <span className={`inline-flex items-center gap-1 font-mono uppercase ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}>
      {children}
    </span>
  );
};
