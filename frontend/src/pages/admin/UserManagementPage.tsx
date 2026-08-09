import React, { useState } from 'react';
import { 
  Users, 
  Search, 
  ShieldCheck, 
  UserCheck, 
  UserX, 
  AlertOctagon, 
  KeyRound, 
  Activity, 
  Award,
  ChevronLeft,
  ChevronRight,
  X
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';

export interface UserItem {
  id: string;
  email: string;
  full_name: string;
  role: 'SUPER_ADMIN' | 'SOC_ANALYST' | 'MODERATOR' | 'AUDITOR' | 'DEVELOPER' | 'USER';
  status: 'ACTIVE' | 'DEACTIVATED' | 'SUSPENDED';
  trust_score: number;
  scans_count: number;
}

export function UserManagementPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [roleFilter, setRoleFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedUser, setSelectedUser] = useState<UserItem | null>(null);
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [showActivityModal, setShowActivityModal] = useState(false);
  const [newRole, setNewRole] = useState<'SUPER_ADMIN' | 'SOC_ANALYST' | 'MODERATOR' | 'AUDITOR' | 'DEVELOPER'>('MODERATOR');

  // Mock Users Database
  const [users, setUsers] = useState<UserItem[]>([
    { id: 'usr_001', email: 'admin@guardianai.io', full_name: 'System Administrator', role: 'SUPER_ADMIN', status: 'ACTIVE', trust_score: 100, scans_count: 142 },
    { id: 'usr_002', email: 'soc_analyst@guardianai.io', full_name: 'SOC Analyst Team', role: 'SOC_ANALYST', status: 'ACTIVE', trust_score: 90, scans_count: 98 },
    { id: 'usr_003', email: 'moderator_1@guardianai.io', full_name: 'Community Moderator', role: 'MODERATOR', status: 'ACTIVE', trust_score: 85, scans_count: 45 },
    { id: 'usr_004', email: 'auditor@guardianai.io', full_name: 'ISO Auditor', role: 'AUDITOR', status: 'ACTIVE', trust_score: 80, scans_count: 12 },
    { id: 'usr_005', email: 'spammer@malicious.com', full_name: 'Spam Bot', role: 'USER', status: 'SUSPENDED', trust_score: 0, scans_count: 2 }
  ]);

  const handleStatusChange = (id: string, newStatus: 'ACTIVE' | 'DEACTIVATED' | 'SUSPENDED') => {
    setUsers(prev => prev.map(u => u.id === id ? { ...u, status: newStatus } : u));
  };

  const handleAssignRole = () => {
    if (!selectedUser) return;
    setUsers(prev => prev.map(u => u.id === selectedUser.id ? { ...u, role: newRole } : u));
    setShowRoleModal(false);
  };

  const filteredUsers = users.filter(u => {
    const matchesSearch = u.email.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          u.full_name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = roleFilter === 'ALL' || u.role === roleFilter;
    const matchesStatus = statusFilter === 'ALL' || u.status === statusFilter;
    return matchesSearch && matchesRole && matchesStatus;
  });

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Users className="w-8 h-8 text-cyan-400" />
            Enterprise User & Role Management Console
          </h1>
          <p className="text-slate-400 mt-1">
            Manage user accounts, assign RBAC permissions, reset credentials, and monitor audit activity trails.
          </p>
        </div>
      </div>

      {/* Search & Filters Bar */}
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search email, full name, user ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-800/90 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 text-sm"
          />
        </div>

        <div className="flex gap-3 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Roles</option>
            <option value="SUPER_ADMIN">SUPER_ADMIN</option>
            <option value="SOC_ANALYST">SOC_ANALYST</option>
            <option value="MODERATOR">MODERATOR</option>
            <option value="AUDITOR">AUDITOR</option>
            <option value="USER">USER</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="ACTIVE">ACTIVE</option>
            <option value="DEACTIVATED">DEACTIVATED</option>
            <option value="SUSPENDED">SUSPENDED</option>
          </select>
        </div>
      </div>

      {/* Users Table */}
      <Card className="p-6 bg-slate-800/60 border-slate-700/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900 text-slate-400 font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3">User Details</th>
                <th className="p-3">RBAC Role</th>
                <th className="p-3">Account Status</th>
                <th className="p-3">Trust Reputation</th>
                <th className="p-3">Scans Run</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredUsers.map(user => (
                <tr key={user.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3">
                    <div className="font-bold text-slate-100">{user.full_name}</div>
                    <div className="text-slate-400 font-mono text-[11px]">{user.email} • {user.id}</div>
                  </td>
                  <td className="p-3">
                    <span className="px-2.5 py-1 rounded-md text-[10px] font-bold font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                      {user.role}
                    </span>
                  </td>
                  <td className="p-3">
                    <Badge variant={user.status === 'ACTIVE' ? 'safe' : 'dangerous'}>
                      {user.status}
                    </Badge>
                  </td>
                  <td className="p-3 font-mono font-bold text-emerald-400 flex items-center gap-1">
                    <Award className="w-3.5 h-3.5 text-amber-400" />
                    {user.trust_score} pts
                  </td>
                  <td className="p-3 font-mono text-slate-300">{user.scans_count}</td>
                  <td className="p-3 text-right space-x-2">
                    <button 
                      onClick={() => { setSelectedUser(user); setShowRoleModal(true); }}
                      className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-md font-semibold"
                    >
                      Assign Role
                    </button>
                    {user.status === 'ACTIVE' ? (
                      <button 
                        onClick={() => handleStatusChange(user.id, 'SUSPENDED')}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-amber-400 rounded-md font-semibold"
                      >
                        Suspend
                      </button>
                    ) : (
                      <button 
                        onClick={() => handleStatusChange(user.id, 'ACTIVE')}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-emerald-400 rounded-md font-semibold"
                      >
                        Activate
                      </button>
                    )}
                    <button 
                      onClick={() => { setSelectedUser(user); setShowActivityModal(true); }}
                      className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-md font-semibold"
                    >
                      Activity
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Role Assignment Modal */}
      {showRoleModal && selectedUser && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-5">
            <h2 className="text-xl font-bold text-cyan-400 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5" />
              Assign Role: {selectedUser.full_name}
            </h2>
            <select
              value={newRole}
              onChange={(e) => setNewRole(e.target.value as any)}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
            >
              <option value="SUPER_ADMIN">SUPER_ADMIN (Unrestricted Access)</option>
              <option value="SOC_ANALYST">SOC_ANALYST (Threat Operations)</option>
              <option value="MODERATOR">MODERATOR (Community Control)</option>
              <option value="AUDITOR">AUDITOR (Compliance & Audit)</option>
              <option value="DEVELOPER">DEVELOPER (API Control)</option>
            </select>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <Button variant="secondary" onClick={() => setShowRoleModal(false)}>Cancel</Button>
              <Button variant="primary" onClick={handleAssignRole}>Assign Role</Button>
            </div>
          </div>
        </div>
      )}

      {/* User Activity Modal */}
      {showActivityModal && selectedUser && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg p-6 shadow-2xl space-y-5">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Activity className="w-5 h-5 text-cyan-400" />
                User Activity Trail: {selectedUser.full_name}
              </h2>
              <button onClick={() => setShowActivityModal(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs text-slate-300">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between">
                <span>LOGIN_SUCCESS</span>
                <span className="text-slate-500">2026-08-01 03:00:00 ISO</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between">
                <span>SUBMIT_SCAM_REPORT (rep_101)</span>
                <span className="text-slate-500">2026-08-01 02:45:00 ISO</span>
              </div>
            </div>

            <div className="flex justify-end pt-3 border-t border-slate-800">
              <Button variant="secondary" onClick={() => setShowActivityModal(false)}>Close</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default UserManagementPage;
