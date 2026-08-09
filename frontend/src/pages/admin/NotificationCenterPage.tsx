import React, { useState } from 'react';
import { 
  Bell, 
  AlertTriangle, 
  ShieldAlert, 
  FileText, 
  CheckCircle2, 
  KeyRound, 
  Mail, 
  Filter, 
  Trash2, 
  CheckCheck,
  Send
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';

export interface NotificationItem {
  id: string;
  category: 'SYSTEM' | 'THREAT' | 'USER_REPORT' | 'MODERATION' | 'API';
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'INFO';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  email_sent: boolean;
}

export function NotificationCenterPage() {
  const [categoryFilter, setCategoryFilter] = useState<string>('ALL');
  const [showBroadcastModal, setShowBroadcastModal] = useState<boolean>(false);
  const [broadcastTitle, setBroadcastTitle] = useState<string>('');
  const [broadcastMessage, setBroadcastMessage] = useState<string>('');
  const [sendEmail, setSendEmail] = useState<boolean>(true);

  const [notifications, setNotifications] = useState<NotificationItem[]>([
    {
      id: 'notif_101',
      category: 'THREAT',
      severity: 'CRITICAL',
      title: 'Digital Arrest Cyber Surge Alert',
      message: 'Detected 42 concurrent fake police calls in Delhi NCR targeting senior citizens.',
      timestamp: '2026-08-01T03:55:00Z',
      read: false,
      email_sent: true
    },
    {
      id: 'notif_102',
      category: 'SYSTEM',
      severity: 'HIGH',
      title: 'PostgreSQL Pool Connection Spike',
      message: 'Active database connections reached 85% of total max pool depth (42/50).',
      timestamp: '2026-08-01T03:40:00Z',
      read: false,
      email_sent: true
    },
    {
      id: 'notif_103',
      category: 'MODERATION',
      severity: 'MEDIUM',
      title: 'Pending Moderation Queue Threshold',
      message: '15 new crowdsourced scam reports require moderator verification.',
      timestamp: '2026-08-01T03:30:00Z',
      read: true,
      email_sent: false
    },
    {
      id: 'notif_104',
      category: 'API',
      severity: 'HIGH',
      title: 'Developer API Key Quota Exhausted',
      message: 'API Key key_enterprise_99 exceeded 1,000,000 requests/day quota.',
      timestamp: '2026-08-01T03:15:00Z',
      read: true,
      email_sent: true
    },
    {
      id: 'notif_105',
      category: 'USER_REPORT',
      severity: 'INFO',
      title: 'New Verified Scam Submitter Upgrade',
      message: 'User usr_senior_99 earned EXPERT trust tier (75 reputation pts).',
      timestamp: '2026-08-01T03:00:00Z',
      read: true,
      email_sent: false
    }
  ]);

  const handleMarkAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const handleClearAll = () => {
    setNotifications([]);
  };

  const handleSendBroadcast = () => {
    if (!broadcastTitle || !broadcastMessage) return;
    const newNotif: NotificationItem = {
      id: `notif_${Date.now().toString().slice(-4)}`,
      category: 'SYSTEM',
      severity: 'CRITICAL',
      title: broadcastTitle,
      message: broadcastMessage,
      timestamp: new Date().toISOString(),
      read: false,
      email_sent: sendEmail
    };
    setNotifications([newNotif, ...notifications]);
    setShowBroadcastModal(false);
    setBroadcastTitle('');
    setBroadcastMessage('');
  };

  const filteredNotifications = notifications.filter(n => {
    if (categoryFilter === 'ALL') return true;
    return n.category === categoryFilter;
  });

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Bell className="w-8 h-8 text-cyan-400" />
            Enterprise Notification & Alert Broadcast Center
          </h1>
          <p className="text-slate-400 mt-1">
            Real-time alert dispatcher monitoring system health, cyber threats, user reports, moderation queues, and API quotas.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" onClick={handleMarkAllRead} className="text-xs">
            <CheckCheck className="w-4 h-4 mr-1" /> Mark All Read
          </Button>
          <Button variant="danger" onClick={handleClearAll} className="text-xs">
            <Trash2 className="w-4 h-4 mr-1" /> Clear All
          </Button>
          <Button variant="primary" onClick={() => setShowBroadcastModal(true)} className="text-xs">
            <Send className="w-4 h-4 mr-1" /> Dispatch Broadcast
          </Button>
        </div>
      </div>

      {/* Category Filters */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {['ALL', 'SYSTEM', 'THREAT', 'USER_REPORT', 'MODERATION', 'API'].map(cat => (
          <button
            key={cat}
            onClick={() => setCategoryFilter(cat)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
              categoryFilter === cat 
                ? 'bg-cyan-500 text-slate-950 shadow-sm' 
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Notifications List Feed */}
      <div className="space-y-4">
        {filteredNotifications.map(n => (
          <Card 
            key={n.id} 
            className={`p-5 transition-all ${
              n.read ? 'bg-slate-800/40 border-slate-800' : 'bg-slate-800/90 border-cyan-500/50 shadow-lg'
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-3">
                  <Badge variant={n.severity === 'CRITICAL' ? 'dangerous' : n.severity === 'HIGH' ? 'caution' : 'safe'}>
                    {n.severity}
                  </Badge>
                  <span className="text-xs font-mono font-bold text-cyan-400">{n.category}</span>
                  {n.email_sent && (
                    <span className="text-[10px] font-mono text-slate-400 flex items-center gap-1 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                      <Mail className="w-3 h-3 text-emerald-400" /> EMAIL DISPATCHED
                    </span>
                  )}
                </div>

                <h3 className="text-base font-bold text-slate-100">{n.title}</h3>
                <p className="text-xs text-slate-300">{n.message}</p>
                <div className="text-[11px] font-mono text-slate-500">{new Date(n.timestamp).toLocaleString()}</div>
              </div>

              {!n.read && (
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shrink-0 mt-2" />
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Dispatch Security Broadcast Modal */}
      {showBroadcastModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-md p-6 shadow-2xl space-y-5">
            <h2 className="text-xl font-bold text-cyan-400 flex items-center gap-2">
              <Send className="w-5 h-5" />
              Dispatch Security Alert Broadcast
            </h2>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Broadcast Title</label>
                <input
                  type="text"
                  placeholder="e.g. Critical Threat Advisory"
                  value={broadcastTitle}
                  onChange={(e) => setBroadcastTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-400 block mb-1">Announcement Details</label>
                <textarea
                  rows={3}
                  placeholder="Details regarding threat vector or system maintenance..."
                  value={broadcastMessage}
                  onChange={(e) => setBroadcastMessage(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="flex items-center gap-2 pt-1">
                <input
                  type="checkbox"
                  id="email_chk"
                  checked={sendEmail}
                  onChange={(e) => setSendEmail(e.target.checked)}
                  className="rounded bg-slate-800 border-slate-700 text-cyan-500 focus:ring-0"
                />
                <label htmlFor="email_chk" className="text-xs text-slate-300 flex items-center gap-1 cursor-pointer">
                  <Mail className="w-3.5 h-3.5 text-emerald-400" /> Dispatch via Email SMTP Service
                </label>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <Button variant="secondary" onClick={() => setShowBroadcastModal(false)}>Cancel</Button>
              <Button variant="primary" onClick={handleSendBroadcast}>Dispatch Announcement</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default NotificationCenterPage;
