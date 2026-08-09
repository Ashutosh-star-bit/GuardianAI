import React, { useState, useEffect, useMemo } from 'react';
import { 
  Search, 
  Users, 
  ShieldAlert, 
  FileCheck, 
  Bell, 
  BarChart3, 
  Settings, 
  X,
  ArrowRight
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export interface SearchResultItem {
  id: string;
  category: 'USERS' | 'REPORTS' | 'THREATS' | 'AUDIT_LOGS' | 'NOTIFICATIONS' | 'ANALYTICS' | 'SETTINGS';
  title: string;
  subtitle: string;
  url: string;
}

interface GlobalAdminSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function GlobalAdminSearchModal({ isOpen, onClose }: GlobalAdminSearchModalProps) {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  // Global Admin Search Index Dataset
  const searchIndex: SearchResultItem[] = useMemo(() => [
    // Users
    { id: 'u_1', category: 'USERS', title: 'System Administrator (admin@guardianai.io)', subtitle: 'SUPER_ADMIN • Active', url: '/admin/users' },
    { id: 'u_2', category: 'USERS', title: 'SOC Analyst Team (soc_analyst@guardianai.io)', subtitle: 'SOC_ANALYST • Active', url: '/admin/users' },
    { id: 'u_3', category: 'USERS', title: 'Community Moderator (moderator_1@guardianai.io)', subtitle: 'MODERATOR • Active', url: '/admin/users' },
    
    // Scam Reports
    { id: 'r_1', category: 'REPORTS', title: 'Fake Police Digital Arrest Scam Call (rep_301)', subtitle: 'DIGITAL_ARREST • Pending Review', url: '/admin/moderation' },
    { id: 'r_2', category: 'REPORTS', title: 'HDFC Bank Account Blocked SMS Link (rep_302)', subtitle: 'PHISHING_URL • Pending Review', url: '/admin/moderation' },
    
    // Threat IOCs
    { id: 't_1', category: 'THREATS', title: 'http://hdfc-kyc-update.top/login', subtitle: 'Phishing URL • Risk Score 98/100', url: '/admin/threat-intel' },
    { id: 't_2', category: 'THREATS', title: 'cbi.police.dept@paytm', subtitle: 'UPI Fraud VPA • ₹4.8L Volume', url: '/admin/threat-intel' },
    
    // Audit Logs
    { id: 'a_1', category: 'AUDIT_LOGS', title: 'Role Assignment Event (log_1001)', subtitle: 'usr_admin_001 assigned MODERATOR role', url: '/admin/audit-logs' },
    { id: 'a_2', category: 'AUDIT_LOGS', title: 'RLHF Fine-Tuning Dataset Export', subtitle: 'guardianai_rlhf_dataset.jsonl', url: '/admin/audit-logs' },

    // Notifications
    { id: 'n_1', category: 'NOTIFICATIONS', title: 'Digital Arrest Cyber Surge Alert', subtitle: 'CRITICAL • Threat Alert', url: '/admin/notifications' },
    { id: 'n_2', category: 'NOTIFICATIONS', title: 'PostgreSQL Pool Connection Spike', subtitle: 'HIGH • System Alert', url: '/admin/notifications' },

    // Analytics & Settings
    { id: 'an_1', category: 'ANALYTICS', title: 'AI LLM Inference Token Metrics', subtitle: 'Gemini Flash & Pro Consumption', url: '/admin/ai-usage' },
    { id: 'an_2', category: 'ANALYTICS', title: 'Infrastructure & System Health', subtitle: 'CPU, RAM, PostgreSQL Telemetry', url: '/admin/system-health' },
    { id: 's_1', category: 'SETTINGS', title: 'Security & Access Control Settings', subtitle: 'MFA & Session Timeout Rules', url: '/settings' }
  ], []);

  // Filter Results
  const results = useMemo(() => {
    if (!query.trim()) return searchIndex.slice(0, 5);
    const q = query.toLowerCase();
    return searchIndex.filter(item => 
      item.title.toLowerCase().includes(q) || 
      item.subtitle.toLowerCase().includes(q) ||
      item.category.toLowerCase().includes(q)
    );
  }, [query, searchIndex]);

  // Keyboard Navigation (Esc to close)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!isOpen) return null;

  const getCategoryIcon = (cat: string) => {
    switch (cat) {
      case 'USERS': return <Users className="w-4 h-4 text-cyan-400" />;
      case 'REPORTS': return <ShieldAlert className="w-4 h-4 text-amber-400" />;
      case 'THREATS': return <ShieldAlert className="w-4 h-4 text-red-400" />;
      case 'AUDIT_LOGS': return <FileCheck className="w-4 h-4 text-emerald-400" />;
      case 'NOTIFICATIONS': return <Bell className="w-4 h-4 text-purple-400" />;
      case 'ANALYTICS': return <BarChart3 className="w-4 h-4 text-indigo-400" />;
      default: return <Settings className="w-4 h-4 text-slate-400" />;
    }
  };

  const handleSelectResult = (targetUrl: string) => {
    navigate(targetUrl);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-start justify-center pt-20 p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col space-y-0">
        {/* Search Bar Input */}
        <div className="p-4 border-b border-slate-800 flex items-center gap-3">
          <Search className="w-5 h-5 text-cyan-400 shrink-0" />
          <input
            type="text"
            autoFocus
            placeholder="Global search across users, reports, threat IOCs, audit logs, notifications..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-slate-100 placeholder-slate-500 focus:outline-none text-sm font-medium"
          />
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 divide-y divide-slate-800/60">
          {results.length > 0 ? (
            results.map(item => (
              <div
                key={item.id}
                onClick={() => handleSelectResult(item.url)}
                className="p-3 hover:bg-slate-800/80 rounded-xl transition-colors cursor-pointer flex items-center justify-between group"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-slate-900 rounded-lg border border-slate-800">
                    {getCategoryIcon(item.category)}
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-100 group-hover:text-cyan-400 transition-colors">
                      {item.title}
                    </div>
                    <div className="text-[11px] text-slate-400 font-mono mt-0.5">{item.subtitle}</div>
                  </div>
                </div>

                <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-cyan-400 transition-colors" />
              </div>
            ))
          ) : (
            <div className="p-8 text-center text-xs text-slate-500 font-mono">
              No matching records found for "{query}".
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="p-3 bg-slate-950 border-t border-slate-800 text-[11px] font-mono text-slate-500 flex justify-between">
          <span>Sub-10ms Unified Index</span>
          <span>Press ESC to close</span>
        </div>
      </div>
    </div>
  );
}
export default GlobalAdminSearchModal;
