import React from 'react';

/**
 * GuardianAI Skeleton UI Component
 * Purpose: Renders pulse placeholder bars for loading states.
 */

interface SkeletonProps {
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className = 'h-4 w-full' }) => {
  return <div className={`bg-slate-800 animate-pulse rounded-lg ${className}`} />;
};
