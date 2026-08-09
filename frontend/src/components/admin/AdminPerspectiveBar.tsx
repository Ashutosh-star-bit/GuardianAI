import React from 'react';
import { ShieldCheck, Eye, Sparkles, RefreshCw } from 'lucide-react';
import { useAuth, SubscriptionTier } from '../../context/AuthContext';

export const AdminPerspectiveBar: React.FC = () => {
  const { isAdmin, activePerspective, switchAdminPerspective, effectiveTier, currentUser } = useAuth();

  if (!isAdmin || !currentUser) return null;

  const tiers: { id: SubscriptionTier | 'DEFAULT'; label: string; badge: string }[] = [
    { id: 'DEFAULT', label: 'Master Admin (Enterprise)', badge: 'UNLIMITED' },
    { id: 'BUSINESS', label: 'Business SMB ($14.99)', badge: 'SMB' },
    { id: 'PRO', label: 'Pro Personal ($4.99)', badge: 'PRO' },
    { id: 'FREE', label: 'Free Tier ($0/mo)', badge: '50 SCANS' },
  ];

  return (
    <div className="bg-gradient-to-r from-amber-950 via-slate-900 to-amber-950 border-b border-amber-500/40 text-amber-200 px-4 py-2 text-xs font-semibold shadow-md z-50">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="bg-amber-500/20 p-1 rounded border border-amber-500/40">
            <ShieldCheck className="w-4 h-4 text-amber-400" />
          </div>
          <span>
            <strong className="text-white font-bold">Admin Account Active:</strong> {currentUser.email}
          </span>
          <span className="bg-amber-400 text-black px-2 py-0.5 rounded font-black text-[10px] uppercase">
            {effectiveTier} MODE
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-slate-400 hidden sm:inline flex items-center gap-1">
            <Eye className="w-3.5 h-3.5 text-amber-400" />
            <span>Switch User Perspective:</span>
          </span>

          <div className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-amber-500/30">
            {tiers.map((t) => {
              const isActive = activePerspective === t.id;
              return (
                <button
                  key={t.id}
                  onClick={() => switchAdminPerspective(t.id)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-extrabold transition-all flex items-center gap-1 ${
                    isActive
                      ? 'bg-amber-400 text-slate-950 shadow-sm'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800'
                  }`}
                  title={`Test platform UI from ${t.label} perspective`}
                >
                  <span>{t.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
