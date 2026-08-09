import React from 'react';
import { AlertTriangle, CheckCircle, Info, XCircle, X } from 'lucide-react';

/**
 * GuardianAI Toast Component
 * Purpose: Renders individual toast alert messages (success, error, warning, info).
 */

export type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastProps {
  type: ToastType;
  title: string;
  message?: string;
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ type, title, message, onClose }) => {
  const icons = {
    success: <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0" />,
    error: <XCircle className="w-5 h-5 text-red-400 shrink-0" />,
    warning: <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />,
    info: <Info className="w-5 h-5 text-sky-400 shrink-0" />,
  };

  const borders = {
    success: 'border-emerald-500/40 bg-emerald-950/90 text-emerald-100',
    error: 'border-red-500/40 bg-red-950/90 text-red-100',
    warning: 'border-amber-500/40 bg-amber-950/90 text-amber-100',
    info: 'border-sky-500/40 bg-sky-950/90 text-sky-100',
  };

  return (
    <div
      className={`flex items-start gap-3 p-4 rounded-xl border backdrop-blur-md shadow-2xl transition-all ${borders[type]}`}
      role="alert"
    >
      {icons[type]}
      <div className="flex-1 text-xs sm:text-sm">
        <h5 className="font-bold leading-tight">{title}</h5>
        {message && <p className="mt-1 opacity-90 leading-relaxed">{message}</p>}
      </div>
      <button
        onClick={onClose}
        className="p-1 hover:bg-white/10 rounded-lg transition-colors text-slate-300"
        aria-label="Close notification"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};
