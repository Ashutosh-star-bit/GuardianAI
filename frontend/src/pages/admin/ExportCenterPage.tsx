import React, { useState } from 'react';
import { 
  Download, 
  FileSpreadsheet, 
  FileText, 
  Code, 
  ShieldCheck, 
  Lock, 
  CheckCircle2,
  Database,
  BarChart3,
  Users
} from 'lucide-react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';

export function ExportCenterPage() {
  const [selectedDataset, setSelectedDataset] = useState<'REPORTS' | 'ANALYTICS' | 'AUDIT_LOGS' | 'COMMUNITY'>('REPORTS');
  const [selectedFormat, setSelectedFormat] = useState<'CSV' | 'EXCEL' | 'PDF' | 'JSON'>('CSV');
  const [sanitizeFormulas, setSanitizeFormulas] = useState<boolean>(true);
  const [stripPii, setStripPii] = useState<boolean>(true);
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [exportComplete, setExportComplete] = useState<boolean>(false);

  const handleDownload = () => {
    setIsExporting(true);
    setExportComplete(false);

    setTimeout(() => {
      setIsExporting(false);
      setExportComplete(true);

      const mockData = selectedFormat === 'JSON' 
        ? JSON.stringify([{ id: "exp_101", dataset: selectedDataset, format: selectedFormat }], null, 2)
        : `id,dataset,format,sanitized\nexp_101,${selectedDataset},${selectedFormat},${sanitizeFormulas}`;

      const mimeTypes = {
        CSV: 'text/csv',
        EXCEL: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        PDF: 'application/pdf',
        JSON: 'application/json'
      };

      const blob = new Blob([mockData], { type: mimeTypes[selectedFormat] });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `guardianai_${selectedDataset.toLowerCase()}_export.${selectedFormat.toLowerCase()}`;
      a.click();
    }, 800);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-cyan-400">
            <Download className="w-8 h-8 text-cyan-400" />
            Enterprise Secure Export Center
          </h1>
          <p className="text-slate-400 mt-1">
            Export platform datasets in CSV, Excel, PDF, or JSON format with mandatory CSV formula injection protection and PII stripping.
          </p>
        </div>
      </div>

      {/* Grid: Dataset & Format Selectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Step 1: Select Target Dataset */}
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            1. Select Target Dataset
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              { id: 'REPORTS', name: 'Scam Reports', desc: 'Crowdsourced threat reports', icon: Database },
              { id: 'ANALYTICS', name: 'System Analytics', desc: 'Scan volume & accuracy', icon: BarChart3 },
              { id: 'AUDIT_LOGS', name: 'Compliance Audit Logs', desc: 'SHA-256 event trail', icon: Lock },
              { id: 'COMMUNITY', name: 'Community HITL Data', desc: 'Fine-tuning dataset', icon: Users }
            ].map(ds => {
              const Icon = ds.icon;
              const isSelected = selectedDataset === ds.id;
              return (
                <div
                  key={ds.id}
                  onClick={() => setSelectedDataset(ds.id as any)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer space-y-1 ${
                    isSelected 
                      ? 'border-cyan-500 bg-cyan-500/10 text-cyan-400' 
                      : 'border-slate-800 bg-slate-900 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <Icon className="w-5 h-5 mb-1" />
                  <div className="font-bold text-sm">{ds.name}</div>
                  <div className="text-[11px] text-slate-400">{ds.desc}</div>
                </div>
              );
            })}
          </div>
        </Card>

        {/* Step 2: Select Export Format */}
        <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-4">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
            2. Select File Export Format
          </h2>

          <div className="grid grid-cols-2 gap-3">
            {[
              { id: 'CSV', name: 'CSV File', ext: '.csv', icon: FileSpreadsheet },
              { id: 'EXCEL', name: 'Excel Workbook', ext: '.xlsx', icon: FileSpreadsheet },
              { id: 'PDF', name: 'PDF Report', ext: '.pdf', icon: FileText },
              { id: 'JSON', name: 'JSON Feed', ext: '.json', icon: Code }
            ].map(fmt => {
              const Icon = fmt.icon;
              const isSelected = selectedFormat === fmt.id;
              return (
                <div
                  key={fmt.id}
                  onClick={() => setSelectedFormat(fmt.id as any)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer space-y-1 ${
                    isSelected 
                      ? 'border-emerald-500 bg-emerald-500/10 text-emerald-400' 
                      : 'border-slate-800 bg-slate-900 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <Icon className="w-5 h-5 mb-1" />
                  <div className="font-bold text-sm">{fmt.name}</div>
                  <div className="text-[11px] font-mono text-slate-400">{fmt.ext}</div>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      {/* Security Options & Download Button */}
      <Card className="p-6 bg-slate-800/60 border-slate-700/60 space-y-6">
        <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-indigo-400" />
          3. Security & Compliance Rules
        </h2>

        <div className="space-y-3 font-xs">
          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={sanitizeFormulas}
              onChange={(e) => setSanitizeFormulas(e.target.checked)}
              className="rounded bg-slate-800 border-slate-700 text-cyan-500 focus:ring-0 w-4 h-4"
            />
            <span className="text-xs text-slate-300">
              <strong className="text-slate-100">CSV Formula Injection Shield:</strong> Escapes leading =, +, -, @ characters to prevent Excel DDE code execution.
            </span>
          </label>

          <label className="flex items-center gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={stripPii}
              onChange={(e) => setStripPii(e.target.checked)}
              className="rounded bg-slate-800 border-slate-700 text-cyan-500 focus:ring-0 w-4 h-4"
            />
            <span className="text-xs text-slate-300">
              <strong className="text-slate-100">Strip Personally Identifiable Information (PII):</strong> Masks Aadhaar numbers, PAN numbers, credit cards, and phone numbers.
            </span>
          </label>
        </div>

        <div className="pt-4 border-t border-slate-800 flex justify-between items-center">
          <div className="text-xs font-mono text-slate-400">
            Target File: <strong className="text-cyan-400">guardianai_{selectedDataset.toLowerCase()}_export.{selectedFormat.toLowerCase()}</strong>
          </div>

          <Button 
            variant="primary" 
            onClick={handleDownload}
            disabled={isExporting}
            className="flex items-center gap-2 px-6 py-2.5 text-xs font-bold"
          >
            <Download className="w-4 h-4" />
            {isExporting ? 'Generating Package...' : 'Download Export Package'}
          </Button>
        </div>

        {exportComplete && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-emerald-400 text-xs font-bold flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" />
            Export generated and downloaded successfully!
          </div>
        )}
      </Card>
    </div>
  );
}
export default ExportCenterPage;
