import React, { useState } from 'react';
import { 
  FileCheck, 
  Search, 
  Download, 
  ShieldCheck, 
  ShieldAlert, 
  Filter, 
  Calendar,
  Lock,
  Terminal
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';

export interface AuditItem {
  id: string;
  timestamp: string;
  actor_id: string;
  action_type: 'LOGIN_SUCCESS' | 'ROLE_ASSIGNED' | 'REPORT_VERIFIED' | 'ACCOUNT_SUSPENDED' | 'API_KEY_REVOKED' | 'BROADCAST_CREATED' | 'RLHF_EXPORT';
  target_resource: string;
  ip_address: string;
  details: string;
  hash_verified: boolean;
}

export function AuditLogsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('ALL');

  const [logs] = useState<AuditItem[]>([
    {
      id: 'log_1001',
      timestamp: '2026-08-01T03:54:12Z',
      actor_id: 'usr_admin_001',
      action_type: 'ROLE_ASSIGNED',
      target_resource: 'usr_003 (MODERATOR)',
      ip_address: '192.168.1.100',
      details: 'Assigned MODERATOR role to user account',
      hash_verified: true
    },
    {
      id: 'log_1002',
      timestamp: '2026-08-01T03:50:00Z',
      actor_id: 'usr_admin_001',
      action_type: 'REPORT_VERIFIED',
      target_resource: 'rep_scam_882',
      ip_address: '192.168.1.100',
      details: 'Verified crowdsourced digital arrest scam report',
      hash_verified: true
    },
    {
      id: 'log_1003',
      timestamp: '2026-08-01T03:45:00Z',
      actor_id: 'usr_admin_001',
      action_type: 'BROADCAST_CREATED',
      target_resource: 'broad_9912',
      ip_address: '192.168.1.100',
      details: 'Dispatched national emergency cyber threat broadcast',
      hash_verified: true
    },
    {
      id: 'log_1004',
      timestamp: '2026-08-01T03:30:00Z',
      actor_id: 'usr_mod_42',
      action_type: 'ACCOUNT_SUSPENDED',
      target_resource: 'usr_spammer_90',
      ip_address: '10.0.4.12',
      details: 'Suspended automated spam report account',
      hash_verified: true
    },
    {
      id: 'log_1005',
      timestamp: '2026-08-01T03:15:00Z',
      actor_id: 'usr_admin_001',
      action_type: 'RLHF_EXPORT',
      target_resource: 'guardianai_rlhf_dataset.jsonl',
      ip_address: '192.168.1.100',
      details: 'Exported verified HITL feedback dataset for model fine-tuning',
      hash_verified: true
    }
  ]);

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.actor_id.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          log.target_resource.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          log.details.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === 'ALL' || log.action_type.includes(categoryFilter);
    return matchesSearch && matchesCategory;
  });

  const handleExport = (format: 'CSV' | 'JSON') => {
    const dataStr = format === 'JSON' 
      ? JSON.stringify(filteredLogs, null, 2)
      : "ID,Timestamp,Actor,Action,Target,IP\n" + filteredLogs.map(l => `${l.id},${l.timestamp},${l.actor_id},${l.action_type},${l.target_resource},${l.ip_address}`).join("\n");

    const blob = new Blob([dataStr], { type: format === 'JSON' ? 'application/json' : 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `guardianai_audit_logs.${format.toLowerCase()}`;
    a.click();
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <FileCheck className="w-8 h-8 text-cyan-400" />
            Immutable Audit Trail & Compliance Console
          </h1>
          <p className="text-slate-400 mt-1">
            Tamper-evident audit log with SHA-256 hash chaining for ISO 27001 & SOC 2 compliance.
          </p>
        </div>

        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => handleExport('CSV')} className="text-xs">
            <Download className="w-4 h-4 mr-1" /> Export CSV
          </Button>
          <Button variant="primary" onClick={() => handleExport('JSON')} className="text-xs">
            <Download className="w-4 h-4 mr-1" /> Export JSON
          </Button>
        </div>
      </div>

      {/* Search & Category Filter Bar */}
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search actor ID, target resource, details..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 text-sm"
          />
        </div>

        <div className="flex gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Action Categories</option>
            <option value="LOGIN">Logins</option>
            <option value="ROLE">Role & Permissions</option>
            <option value="REPORT">Report Approvals</option>
            <option value="ACCOUNT">Account Actions</option>
            <option value="BROADCAST">System Broadcasts</option>
            <option value="EXPORT">Data Exports</option>
          </select>
        </div>
      </div>

      {/* Immutable Audit Log Table */}
      <Card className="p-6 bg-slate-800/60 border-slate-700/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">Timestamp (ISO)</th>
                <th className="p-3">Actor ID</th>
                <th className="p-3">Action Type</th>
                <th className="p-3">Target Resource</th>
                <th className="p-3">IP Address</th>
                <th className="p-3">Integrity Check</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 font-mono">
              {filteredLogs.map(log => (
                <tr key={log.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3 text-slate-400">{log.timestamp}</td>
                  <td className="p-3 font-bold text-cyan-400">{log.actor_id}</td>
                  <td className="p-3">
                    <span className="px-2 py-1 bg-slate-900 border border-slate-700 rounded text-[10px] font-bold text-slate-200">
                      {log.action_type}
                    </span>
                  </td>
                  <td className="p-3 text-slate-100">{log.target_resource}</td>
                  <td className="p-3 text-slate-400">{log.ip_address}</td>
                  <td className="p-3">
                    {log.hash_verified ? (
                      <span className="inline-flex items-center gap-1 text-emerald-400 text-[11px] font-semibold">
                        <ShieldCheck className="w-3.5 h-3.5" /> SHA256 VERIFIED
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-rose-400 text-[11px] font-semibold">
                        <ShieldAlert className="w-3.5 h-3.5" /> TAMPER DETECTED
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
export default AuditLogsPage;
