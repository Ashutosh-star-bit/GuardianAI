import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Check, 
  X, 
  GitMerge, 
  AlertOctagon, 
  Search, 
  Award, 
  FileText,
  User,
  History,
  CheckSquare,
  Square,
  Sliders
} from 'lucide-react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';

export interface AdminReportItem {
  id: string;
  user_id: string;
  user_trust_score: number;
  user_trust_tier: 'NOVICE' | 'TRUSTED' | 'EXPERT' | 'MODERATOR';
  title: string;
  description: string;
  category: string;
  status: 'PENDING' | 'UNDER_REVIEW' | 'VERIFIED' | 'REJECTED' | 'MERGED';
  is_spam: boolean;
  upvotes: number;
  downvotes: number;
  created_at: string;
}

export interface AuditLogEntry {
  id: string;
  moderator_id: string;
  action: 'APPROVE' | 'REJECT' | 'MERGE' | 'FLAG_SPAM' | 'ADJUST_TRUST';
  report_id: string;
  timestamp: string;
}

export function AdminModerationPanelPage() {
  const [activeTab, setActiveTab] = useState<'pending' | 'spam' | 'duplicates' | 'audit_log' | 'reputation_leaderboard'>('pending');
  const [statusFilter, setStatusFilter] = useState<string>('PENDING');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedReportIds, setSelectedReportIds] = useState<string[]>([]);
  const [showMergeModal, setShowMergeModal] = useState<boolean>(false);
  const [showTrustModal, setShowTrustModal] = useState<boolean>(false);
  const [primaryReportId, setPrimaryReportId] = useState<string>('');
  const [targetUser, setTargetUser] = useState<AdminReportItem | null>(null);
  const [trustAdjustment, setTrustAdjustment] = useState<number>(5);

  // Initial reports database
  const [reports, setReports] = useState<AdminReportItem[]>([
    {
      id: 'rep_301',
      user_id: 'usr_senior_99',
      user_trust_score: 75,
      user_trust_tier: 'EXPERT',
      title: 'Fake Police Digital Arrest Scam Call',
      description: 'Scammer claimed to be a CBI officer from Delhi police HQ threatening digital arrest unless 50000 rupees was transferred via UPI.',
      category: 'DIGITAL_ARREST',
      status: 'PENDING',
      is_spam: false,
      upvotes: 14,
      downvotes: 1,
      created_at: new Date().toISOString()
    },
    {
      id: 'rep_302',
      user_id: 'usr_novice_12',
      user_trust_score: 20,
      user_trust_tier: 'NOVICE',
      title: 'HDFC Bank Account Blocked SMS Link',
      description: 'Received SMS stating account blocked with link http://hdfc-verify.top.',
      category: 'PHISHING_URL',
      status: 'PENDING',
      is_spam: false,
      upvotes: 8,
      downvotes: 0,
      created_at: new Date().toISOString()
    },
    {
      id: 'rep_303',
      user_id: 'usr_troll_01',
      user_trust_score: 5,
      user_trust_tier: 'NOVICE',
      title: 'Free Pizza Promo Click Here',
      description: 'Buy cheap shoes and get free pizza now at scam.site.',
      category: 'OTHER',
      status: 'PENDING',
      is_spam: true,
      upvotes: 0,
      downvotes: 12,
      created_at: new Date().toISOString()
    }
  ]);

  // Audit Logs
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>([
    {
      id: 'log_001',
      moderator_id: 'mod_admin_master',
      action: 'APPROVE',
      report_id: 'rep_290',
      timestamp: new Date(Date.now() - 3600000).toISOString()
    }
  ]);

  const logAction = (action: 'APPROVE' | 'REJECT' | 'MERGE' | 'FLAG_SPAM' | 'ADJUST_TRUST', reportId: string) => {
    const newLog: AuditLogEntry = {
      id: `log_${Date.now().toString().slice(-6)}`,
      moderator_id: 'mod_admin_master',
      action: action,
      report_id: reportId,
      timestamp: new Date().toISOString()
    };
    setAuditLogs([newLog, ...auditLogs]);
  };

  const handleApprove = (id: string) => {
    setReports(prev => prev.map(r => r.id === id ? { ...r, status: 'VERIFIED', is_spam: false } : r));
    logAction('APPROVE', id);
  };

  const handleReject = (id: string) => {
    setReports(prev => prev.map(r => r.id === id ? { ...r, status: 'REJECTED' } : r));
    logAction('REJECT', id);
  };

  const handleFlagSpam = (id: string) => {
    setReports(prev => prev.map(r => r.id === id ? { ...r, status: 'REJECTED', is_spam: true } : r));
    logAction('FLAG_SPAM', id);
  };

  const handleToggleSelect = (id: string) => {
    if (selectedReportIds.includes(id)) {
      setSelectedReportIds(selectedReportIds.filter(i => i !== id));
    } else {
      setSelectedReportIds([...selectedReportIds, id]);
    }
  };

  const handleBulkApprove = () => {
    setReports(prev => prev.map(r => selectedReportIds.includes(r.id) ? { ...r, status: 'VERIFIED' } : r));
    selectedReportIds.forEach(id => logAction('APPROVE', id));
    setSelectedReportIds([]);
  };

  const handleBulkReject = () => {
    setReports(prev => prev.map(r => selectedReportIds.includes(r.id) ? { ...r, status: 'REJECTED' } : r));
    selectedReportIds.forEach(id => logAction('REJECT', id));
    setSelectedReportIds([]);
  };

  const handleBulkSpam = () => {
    setReports(prev => prev.map(r => selectedReportIds.includes(r.id) ? { ...r, status: 'REJECTED', is_spam: true } : r));
    selectedReportIds.forEach(id => logAction('FLAG_SPAM', id));
    setSelectedReportIds([]);
  };

  const handleExecuteMerge = () => {
    if (!primaryReportId) return;
    setReports(prev => prev.map(r => {
      if (selectedReportIds.includes(r.id) && r.id !== primaryReportId) {
        return { ...r, status: 'MERGED' };
      }
      return r;
    }));
    logAction('MERGE', primaryReportId);
    setShowMergeModal(false);
    setSelectedReportIds([]);
  };

  const handleApplyTrustScore = () => {
    if (!targetUser) return;
    setReports(prev => prev.map(r => r.user_id === targetUser.user_id ? { ...r, user_trust_score: Math.max(0, Math.min(100, r.user_trust_score + trustAdjustment)) } : r));
    logAction('ADJUST_TRUST', targetUser.user_id);
    setShowTrustModal(false);
  };

  const filteredReports = reports.filter(r => {
    if (activeTab === 'spam') return r.is_spam;
    if (activeTab === 'duplicates') return r.status === 'MERGED';
    
    const matchesStatus = statusFilter === 'ALL' || r.status === statusFilter;
    const matchesSearch = r.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          r.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          r.user_id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-emerald-400">
            <ShieldCheck className="w-8 h-8 text-emerald-400" />
            Admin & Moderator Operations Console
          </h1>
          <p className="text-slate-400 mt-1">
            Review moderation queues, merge duplicate IOCs, flag spam, and monitor user trust reputation.
          </p>
        </div>

        {/* Bulk Action Controls Toolbar */}
        {selectedReportIds.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 bg-slate-800 p-2.5 rounded-xl border border-slate-700">
            <span className="text-xs font-bold text-slate-300 px-2">{selectedReportIds.length} Selected</span>
            <Button size="sm" variant="primary" onClick={handleBulkApprove} className="flex items-center gap-1 text-xs">
              <Check className="w-3.5 h-3.5" /> Approve Bulk
            </Button>
            <Button size="sm" variant="secondary" onClick={handleBulkReject} className="flex items-center gap-1 text-xs">
              <X className="w-3.5 h-3.5" /> Reject Bulk
            </Button>
            <Button size="sm" variant="danger" onClick={handleBulkSpam} className="flex items-center gap-1 text-xs">
              <AlertOctagon className="w-3.5 h-3.5" /> Flag Spam
            </Button>
            <Button size="sm" variant="secondary" onClick={() => setShowMergeModal(true)} className="flex items-center gap-1 text-xs">
              <GitMerge className="w-3.5 h-3.5" /> Merge Selected
            </Button>
          </div>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-6 overflow-x-auto">
        {[
          { key: 'pending', label: 'Pending Queue', icon: FileText },
          { key: 'spam', label: 'Spam Queue', icon: AlertOctagon },
          { key: 'duplicates', label: 'Merged Duplicates', icon: GitMerge },
          { key: 'audit_log', label: 'Moderation Audit Log', icon: History },
          { key: 'reputation_leaderboard', label: 'User Trust Scores', icon: Award }
        ].map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center gap-2 pb-3 text-sm font-semibold transition-colors border-b-2 whitespace-nowrap ${
                activeTab === tab.key
                  ? 'border-emerald-400 text-emerald-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* MODERATION QUEUE CONTENT */}
      {(activeTab === 'pending' || activeTab === 'spam' || activeTab === 'duplicates') && (
        <div className="space-y-6">
          {/* Controls & Filter Pills */}
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative w-full md:w-96">
              <Search className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
              <input
                type="text"
                placeholder="Search reports, user IDs, keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 text-sm"
              />
            </div>
          </div>

          {/* Queue List */}
          <div className="space-y-4">
            {filteredReports.map(report => {
              const isSelected = selectedReportIds.includes(report.id);
              return (
                <Card key={report.id} className={`p-5 transition-all ${isSelected ? 'border-emerald-500 bg-slate-800/90' : 'bg-slate-800/50 border-slate-700/60'}`}>
                  <div className="flex items-start gap-4">
                    <button onClick={() => handleToggleSelect(report.id)} className="mt-1 text-slate-400 hover:text-emerald-400">
                      {isSelected ? <CheckSquare className="w-5 h-5 text-emerald-400" /> : <Square className="w-5 h-5" />}
                    </button>

                    <div className="flex-1 space-y-3">
                      <div className="flex flex-wrap items-center gap-3">
                        <Badge variant={report.status === 'VERIFIED' ? 'safe' : report.status === 'REJECTED' ? 'dangerous' : 'caution'}>
                          {report.status}
                        </Badge>
                        <span className="text-xs font-mono text-cyan-400">{report.category}</span>
                        <div 
                          onClick={() => { setTargetUser(report); setShowTrustModal(true); }}
                          className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-900 px-2.5 py-1 rounded-md border border-slate-800 cursor-pointer hover:border-emerald-500/50"
                        >
                          <User className="w-3.5 h-3.5 text-amber-400" />
                          <span>{report.user_id}</span>
                          <span className="font-mono text-emerald-400 font-bold">({report.user_trust_score} pts • {report.user_trust_tier})</span>
                        </div>
                      </div>

                      <div>
                        <h3 className="text-base font-bold text-slate-100">{report.title}</h3>
                        <p className="text-sm text-slate-300 mt-1">{report.description}</p>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center gap-3 pt-2">
                        <Button size="sm" variant="primary" onClick={() => handleApprove(report.id)} className="flex items-center gap-1">
                          <Check className="w-4 h-4" /> Approve
                        </Button>
                        <Button size="sm" variant="secondary" onClick={() => handleReject(report.id)} className="flex items-center gap-1">
                          <X className="w-4 h-4" /> Reject
                        </Button>
                        <Button size="sm" variant="danger" onClick={() => handleFlagSpam(report.id)} className="flex items-center gap-1">
                          <AlertOctagon className="w-4 h-4" /> Flag Spam
                        </Button>
                      </div>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* AUDIT LOG TAB */}
      {activeTab === 'audit_log' && (
        <Card className="p-6 bg-slate-800/60 border-slate-700/60">
          <h2 className="text-lg font-bold text-slate-100 mb-4 flex items-center gap-2">
            <History className="w-5 h-5 text-emerald-400" />
            Moderator Actions Audit Trail
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-3">Log ID</th>
                  <th className="p-3">Moderator ID</th>
                  <th className="p-3">Action Executed</th>
                  <th className="p-3">Target ID</th>
                  <th className="p-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 font-mono">
                {auditLogs.map(log => (
                  <tr key={log.id} className="hover:bg-slate-800/40">
                    <td className="p-3 text-slate-400">{log.id}</td>
                    <td className="p-3 text-cyan-400">{log.moderator_id}</td>
                    <td className="p-3">
                      <span className={`font-bold ${log.action === 'APPROVE' ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="p-3 text-slate-200">{log.report_id}</td>
                    <td className="p-3 text-slate-400">{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Merge Modal */}
      {showMergeModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-5">
            <h2 className="text-xl font-bold text-emerald-400 flex items-center gap-2">
              <GitMerge className="w-5 h-5" />
              Merge Duplicate Reports
            </h2>
            <p className="text-xs text-slate-400">
              Select primary target report ID to receive combined evidence from {selectedReportIds.length} selected duplicate items:
            </p>

            <select
              value={primaryReportId}
              onChange={(e) => setPrimaryReportId(e.target.value)}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-emerald-500"
            >
              <option value="">Select Primary Target Report...</option>
              {selectedReportIds.map(id => (
                <option key={id} value={id}>{id}</option>
              ))}
            </select>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <Button variant="secondary" onClick={() => setShowMergeModal(false)}>Cancel</Button>
              <Button variant="primary" onClick={handleExecuteMerge} disabled={!primaryReportId}>
                Execute Merge
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* User Trust Modal */}
      {showTrustModal && targetUser && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-5">
            <h2 className="text-xl font-bold text-amber-400 flex items-center gap-2">
              <Award className="w-5 h-5" />
              Adjust Trust Score: {targetUser.user_id}
            </h2>
            <p className="text-xs text-slate-400">
              Current Trust Score: <strong className="text-emerald-400">{targetUser.user_trust_score} pts</strong>
            </p>

            <div className="flex items-center gap-3">
              <button onClick={() => setTrustAdjustment(-10)} className="px-3 py-2 bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-xl text-xs font-bold">-10 Spam</button>
              <button onClick={() => setTrustAdjustment(5)} className="px-3 py-2 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-xl text-xs font-bold">+5 Approved</button>
              <button onClick={() => setTrustAdjustment(20)} className="px-3 py-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-xl text-xs font-bold">+20 Expert</button>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <Button variant="secondary" onClick={() => setShowTrustModal(false)}>Cancel</Button>
              <Button variant="primary" onClick={handleApplyTrustScore}>Apply Score Adjustment</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default AdminModerationPanelPage;
