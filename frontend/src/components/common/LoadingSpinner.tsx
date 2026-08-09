import React from 'react';
import { Shield, Loader2 } from 'lucide-react';

/**
 * GuardianAI Loading Component
 * Purpose: Renders full-page or inline pulse loading spinners with optional contextual progress messaging.
 */

interface LoadingSpinnerProps {
  label?: string;
  fullPage?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  label = 'Loading GuardianAI Platform...',
  fullPage = false,
}) => {
  const content = (
    <div className="flex flex-col items-center justify-center space-y-4 text-center p-8">
      <div className="relative flex items-center justify-center">
        <div className="w-16 h-16 rounded-full border-4 border-sky-500/20 border-t-sky-500 animate-spin"></div>
        <Shield className="w-8 h-8 text-sky-400 absolute" />
      </div>
      <p className="text-sm font-medium text-slate-300 animate-pulse">{label}</p>
    </div>
  );

  if (fullPage) {
    return (
      <div className="fixed inset-0 bg-slate-950/90 backdrop-blur-sm z-50 flex items-center justify-center">
        {content}
      </div>
    );
  }

  return content;
};
