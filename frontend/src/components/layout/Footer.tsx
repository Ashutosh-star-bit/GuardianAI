import React from 'react';
import { ShieldCheck } from 'lucide-react';

/**
 * GuardianAI Footer Component
 * Purpose: Renders bottom platform copyright and privacy assurance information.
 */

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800 bg-slate-950 py-6 px-4 text-center text-xs text-slate-500 mt-auto">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-slate-400">
          <ShieldCheck className="w-4 h-4 text-sky-400" />
          <span className="font-semibold text-white">GuardianAI</span> — Zero-Knowledge Privacy Guaranteed
        </div>
        <p>© 2026 GuardianAI Platform. All rights reserved.</p>
      </div>
    </footer>
  );
};
