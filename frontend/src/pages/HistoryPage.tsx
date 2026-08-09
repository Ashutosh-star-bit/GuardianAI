import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  Search,
  Trash2,
  Download,
  MessageSquare,
  Globe,
  Mail,
  QrCode,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  ArrowRight,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAuth, ScanRecordItem } from '../context/AuthContext';

export const HistoryPage: React.FC = () => {
  const { scanHistory, clearScanHistory } = useAuth();
  const { showToast } = useToast();

  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState<'all' | 'safe' | 'caution' | 'dangerous'>('all');

  const filteredHistory = useMemo(() => {
    return scanHistory.filter((item) => {
      const matchesSearch =
        item.payloadSnippet.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.payloadType.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.plainRationale.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesRisk = riskFilter === 'all' || item.riskBand === riskFilter;

      return matchesSearch && matchesRisk;
    });
  }, [scanHistory, searchTerm, riskFilter]);

  const handleExportCsv = () => {
    if (scanHistory.length === 0) {
      showToast('info', 'No Data', 'Scan history log is empty.');
      return;
    }

    const headers = ['Scan ID', 'Timestamp', 'Channel', 'Threat Score', 'Risk Band', 'Snippet', 'Rationale'];
    const rows = scanHistory.map((s) => [
      s.id,
      s.timestamp,
      s.payloadType,
      s.threatScore,
      s.riskBand,
      `"${s.payloadSnippet.replace(/"/g, '""')}"`,
      `"${s.plainRationale.replace(/"/g, '""')}"`,
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `GuardianAI_Scan_History_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('success', 'Export Complete', 'Exported scan history log to CSV file.');
  };

  const getChannelIcon = (type: string) => {
    if (type.toLowerCase().includes('email')) return Mail;
    if (type.toLowerCase().includes('url')) return Globe;
    if (type.toLowerCase().includes('qr')) return QrCode;
    return MessageSquare;
  };

  return (
    <PageTransition className="space-y-6 py-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
            <History className="w-4 h-4" />
            <span>Audit Trail & Telemetry</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Real Scan History Log</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Real-time audit trail of all threat analysis scans conducted during your active session.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            onClick={handleExportCsv}
            disabled={scanHistory.length === 0}
            variant="secondary"
            className="flex items-center gap-2 text-xs py-2 px-3 font-bold"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </Button>

          <Button
            onClick={() => {
              clearScanHistory();
              showToast('info', 'History Cleared', 'Real scan history log has been cleared.');
            }}
            disabled={scanHistory.length === 0}
            variant="secondary"
            className="bg-red-500/10 hover:bg-red-500/20 text-red-400 border-red-500/30 flex items-center gap-2 text-xs py-2 px-3 font-bold"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear History</span>
          </Button>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search scan payload, channel, or rationale..."
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 outline-none focus:border-sky-400"
          />
        </div>

        <div className="flex items-center gap-2">
          {(['all', 'dangerous', 'caution', 'safe'] as const).map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold uppercase transition-all ${
                riskFilter === r
                  ? r === 'dangerous'
                    ? 'bg-red-500/20 border border-red-500/40 text-red-400'
                    : r === 'caution'
                    ? 'bg-amber-500/20 border border-amber-500/40 text-amber-400'
                    : r === 'safe'
                    ? 'bg-emerald-500/20 border border-emerald-500/40 text-emerald-400'
                    : 'bg-sky-500/20 border border-sky-500/40 text-sky-400'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* Real Scan History Table */}
      {filteredHistory.length === 0 ? (
        <Card className="text-center py-12 space-y-4 border-slate-800 bg-slate-900/90">
          <div className="w-14 h-14 bg-sky-500/10 border border-sky-500/30 rounded-2xl flex items-center justify-center mx-auto text-sky-400">
            <History className="w-7 h-7" />
          </div>
          <h3 className="text-lg font-black text-white">No Scan Records Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            You have not executed any threat analysis scans yet in this session. Run your first inspection below!
          </p>
          <div className="flex justify-center gap-3 pt-2">
            <Link to="/scan/message">
              <Button className="bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-xs py-2 px-4 rounded-xl">
                Run Message Scan
              </Button>
            </Link>
            <Link to="/scan/url">
              <Button variant="secondary" className="text-xs py-2 px-4 rounded-xl">
                Run URL Scan
              </Button>
            </Link>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredHistory.map((item) => {
            const Icon = getChannelIcon(item.payloadType);
            const isDangerous = item.riskBand === 'dangerous';
            const isCaution = item.riskBand === 'caution';

            return (
              <Card
                key={item.id}
                className={`p-4 border transition-all ${
                  isDangerous
                    ? 'border-red-500/40 bg-red-950/10'
                    : isCaution
                    ? 'border-amber-500/40 bg-amber-950/10'
                    : 'border-slate-800 bg-slate-900/90'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <div
                      className={`p-2.5 rounded-xl border shrink-0 ${
                        isDangerous
                          ? 'bg-red-500/10 border-red-500/30 text-red-400'
                          : isCaution
                          ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                          : 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                    </div>

                    <div className="space-y-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-white">{item.payloadType}</span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          {new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300 font-mono line-clamp-1 break-all">
                        {item.payloadSnippet}
                      </p>
                      <p className="text-[11px] text-slate-400 line-clamp-2">
                        {item.plainRationale}
                      </p>
                    </div>
                  </div>

                  <div className="flex sm:flex-col items-center sm:items-end justify-between shrink-0 gap-1 border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-800">
                    <div className="flex items-center gap-1.5">
                      <span className="text-xs font-black text-slate-400">Score:</span>
                      <span
                        className={`text-sm font-black font-mono ${
                          isDangerous ? 'text-red-400' : isCaution ? 'text-amber-400' : 'text-emerald-400'
                        }`}
                      >
                        {item.threatScore}/100
                      </span>
                    </div>

                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-black uppercase ${
                        isDangerous
                          ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                          : isCaution
                          ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      }`}
                    >
                      {item.riskBand}
                    </span>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </PageTransition>
  );
};
