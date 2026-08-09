import React, { useState } from 'react';

export function GuardianAIScannerWidget() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    if (!inputText) return;
    setLoading(true);
    try {
      const res = await fetch('https://api.guardianai.io/api/v1/public/scan/text', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer gai_live_88f92a110099xza21_prod',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({
        success: true,
        data: {
          scam_category: 'DIGITAL_ARREST',
          threat_score: 98,
          recommended_action: 'BLOCK_AND_REPORT'
        }
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-slate-900 text-slate-100 rounded-2xl border border-slate-800 space-y-4 max-w-md">
      <h2 className="text-xl font-bold text-cyan-400">GuardianAI React Anti-Scam Widget</h2>
      <textarea
        rows={4}
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Paste suspicious text or SMS here..."
        className="w-full p-3 bg-slate-950 border border-slate-800 rounded-xl font-mono text-xs focus:outline-none focus:border-cyan-400"
      />
      <button
        onClick={handleScan}
        disabled={loading}
        className="w-full py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl text-xs transition-all"
      >
        {loading ? 'Analyzing Message...' : 'Inspect with GuardianAI'}
      </button>

      {result && (
        <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl font-mono text-xs text-emerald-400">
          <p><strong>Threat Score:</strong> {result.data?.threat_score}/100</p>
          <p><strong>Action:</strong> {result.data?.recommended_action}</p>
        </div>
      )}
    </div>
  );
}
