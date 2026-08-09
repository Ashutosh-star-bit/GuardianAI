import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  TrendingUp,
  ThumbsUp,
  ThumbsDown,
  Search,
  Plus,
  AlertTriangle,
  X,
  ShieldCheck,
  CheckCircle2,
  Share2,
} from 'lucide-react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { ThreeDCard } from '../components/3d/ThreeDCard';

export interface VerifiedScammerThreat {
  id: string;
  title: string;
  scamType: 'DIGITAL_ARREST' | 'BANK_APK_SMISHING' | 'TELEGRAM_PARTTIME' | 'ELECTRICITY_BILL' | 'TYPOSQUATTED_BANK';
  scammerHandleOrNumber: string;
  description: string;
  rawPayloadSnippet: string;
  status: 'VERIFIED_DANGEROUS' | 'UNDER_INVESTIGATION';
  upvotes: number;
  downvotes: number;
  userVote: 'like' | 'dislike' | null;
  reportedDate: string;
}

const INITIAL_COMMUNITY_THREATS: VerifiedScammerThreat[] = [
  {
    id: 'thr_101',
    title: 'Fake CBI/Police Digital Arrest Money Laundering Call',
    scamType: 'DIGITAL_ARREST',
    scammerHandleOrNumber: '+91 98765 43210 (WhatsApp Video Call)',
    description: 'Impersonated Delhi Crime Branch Police Officer. Threatened victim with immediate 7-day digital arrest for illegal FedEx narcotics parcel unless ₹75,000 was transferred via UPI.',
    rawPayloadSnippet: 'Your Aadhaar is linked to illegal money laundering. Pay ₹75000 immediately to clear charges or police will raid your house.',
    status: 'VERIFIED_DANGEROUS',
    upvotes: 142,
    downvotes: 3,
    userVote: null,
    reportedDate: '2026-08-08T18:30:00Z',
  },
  {
    id: 'thr_102',
    title: 'Fake SBI KYC Update Malicious APK Download Link',
    scamType: 'BANK_APK_SMISHING',
    scammerHandleOrNumber: 'SMS Header: VK-SBIBNK',
    description: 'Sends SMS claiming SBI NetBanking account will be suspended in 24 hours. Instructs user to download "SBI_KYC_Update.apk" which steals OTPs and banking credentials.',
    rawPayloadSnippet: 'Dear SBI Customer, your YONO account is suspended today. Update PAN immediately via app: http://sbi-kyc-net.apk',
    status: 'VERIFIED_DANGEROUS',
    upvotes: 98,
    downvotes: 1,
    userVote: null,
    reportedDate: '2026-08-08T14:15:00Z',
  },
  {
    id: 'thr_103',
    title: 'Telegram YouTube Like & Earn Part-Time Income Scam',
    scamType: 'TELEGRAM_PARTTIME',
    scammerHandleOrNumber: 'Telegram Handle: @HR_Recruiter_Maya',
    description: 'Promises ₹500/day for liking YouTube videos. After initial ₹150 payout, demands ₹5,000 "crypto investment task" deposit before withholding funds.',
    rawPayloadSnippet: 'Earn ₹3000-5000 daily from home by reviewing hotels & liking videos. Join Telegram channel: t.me/global_task_work',
    status: 'VERIFIED_DANGEROUS',
    upvotes: 87,
    downvotes: 4,
    userVote: null,
    reportedDate: '2026-08-07T20:45:00Z',
  },
  {
    id: 'thr_104',
    title: 'Electricity Power Disconnection Threat SMS',
    scamType: 'ELECTRICITY_BILL',
    scammerHandleOrNumber: 'SMS / Call: +91 91234 56789',
    description: 'Claims tonight electricity power will be disconnected at 9:30 PM due to previous month unpaid bill. Gives personal mobile number for instant WhatsApp resolution.',
    rawPayloadSnippet: 'Dear Customer your Power supply will be disconnected tonight at 9:30 pm from electricity office because your bill was not updated. Contact Officer 9123456789 immediately.',
    status: 'VERIFIED_DANGEROUS',
    upvotes: 115,
    downvotes: 2,
    userVote: null,
    reportedDate: '2026-08-07T11:20:00Z',
  },
];

export const CommunityDashboardPage: React.FC = () => {
  const { showToast } = useToast();
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('ALL');

  const [threats, setThreats] = useState<VerifiedScammerThreat[]>(() => {
    const saved = localStorage.getItem('guardianai_community_threats_feed');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return INITIAL_COMMUNITY_THREATS;
      }
    }
    return INITIAL_COMMUNITY_THREATS;
  });

  // Save to localStorage whenever threats or votes change
  useEffect(() => {
    localStorage.setItem('guardianai_community_threats_feed', JSON.stringify(threats));
  }, [threats]);

  // Handle Single-Vote Upvote (Like) / Downvote (Dislike)
  const handleVote = (id: string, voteType: 'like' | 'dislike') => {
    setThreats((prev) =>
      prev.map((item) => {
        if (item.id !== id) return item;

        let newUpvotes = item.upvotes;
        let newDownvotes = item.downvotes;
        let newVote: 'like' | 'dislike' | null = voteType;

        if (item.userVote === voteType) {
          // Toggle off if clicking same vote again
          newVote = null;
          if (voteType === 'like') newUpvotes = Math.max(0, newUpvotes - 1);
          if (voteType === 'dislike') newDownvotes = Math.max(0, newDownvotes - 1);
        } else {
          // If switching vote from dislike to like
          if (item.userVote === 'dislike') {
            newDownvotes = Math.max(0, newDownvotes - 1);
          }
          // If switching vote from like to dislike
          if (item.userVote === 'like') {
            newUpvotes = Math.max(0, newUpvotes - 1);
          }

          if (voteType === 'like') newUpvotes += 1;
          if (voteType === 'dislike') newDownvotes += 1;
        }

        return {
          ...item,
          upvotes: newUpvotes,
          downvotes: newDownvotes,
          userVote: newVote,
        };
      })
    );

    showToast('info', 'Vote Recorded', `Your feedback has been reflected in community threat intelligence.`);
  };

  const filteredThreats = threats.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.scammerHandleOrNumber.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesCategory = categoryFilter === 'ALL' || item.scamType === categoryFilter;

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6 py-4">
      {/* Header */}
      <div className="border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
          <ShieldAlert className="w-4 h-4" />
          <span>Real-Time Verified Scammer Intelligence</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">Community Intel Threat Feed</h1>
        <p className="text-xs sm:text-sm text-slate-400">
          Verified active scammer handles, smishing numbers, and fraud vectors reported by users and verified by AI.
        </p>
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search scammer phone number, WhatsApp handle, or fraud type..."
            className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 outline-none focus:border-sky-400"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto">
          {['ALL', 'DIGITAL_ARREST', 'BANK_APK_SMISHING', 'TELEGRAM_PARTTIME', 'ELECTRICITY_BILL'].map((cat) => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={`px-3 py-1.5 rounded-xl text-[11px] font-bold whitespace-nowrap transition-all ${
                categoryFilter === cat
                  ? 'bg-sky-500 text-slate-950 font-black'
                  : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {filteredThreats.map((item) => {
          const totalVotes = item.upvotes + item.downvotes;
          const seriousnessPercent = totalVotes > 0 ? Math.round((item.upvotes / totalVotes) * 100) : 100;

          return (
            <ThreeDCard key={item.id} glowColor="amber" intensity={10}>
              <Card className="p-5 border-slate-800 bg-slate-900/90 backdrop-blur-xl space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="bg-red-500/20 text-red-400 border border-red-500/40 text-[10px] font-black uppercase px-2 py-0.5 rounded">
                        VERIFIED SCAMMER THREAT
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">
                        Reported {new Date(item.reportedDate).toLocaleDateString()}
                      </span>
                    </div>
                    <h3 className="text-base font-black text-white">{item.title}</h3>
                    <div className="text-xs text-sky-400 font-mono font-bold">
                      Target Handle/Number: {item.scammerHandleOrNumber}
                    </div>
                  </div>

                  <div className="bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-xl text-center shrink-0">
                    <div className="text-[10px] text-slate-400 font-bold uppercase">Threat Seriousness</div>
                    <div className="text-base font-black text-red-400 font-mono">{seriousnessPercent}% Verified</div>
                  </div>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">{item.description}</p>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-xl space-y-1 font-mono text-xs">
                  <div className="text-[10px] text-slate-500 uppercase font-bold">Raw Suspicious Payload Snippet</div>
                  <div className="text-slate-300 line-clamp-2">"{item.rawPayloadSnippet}"</div>
                </div>

                <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleVote(item.id, 'like')}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                        item.userVote === 'like'
                          ? 'bg-emerald-500 text-slate-950 font-black shadow-md shadow-emerald-500/20'
                          : 'bg-slate-950 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      <ThumbsUp className="w-3.5 h-3.5" />
                      <span>Confirm Threat ({item.upvotes})</span>
                    </button>

                    <button
                      onClick={() => handleVote(item.id, 'dislike')}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                        item.userVote === 'dislike'
                          ? 'bg-red-500 text-white font-black shadow-md shadow-red-500/20'
                          : 'bg-slate-950 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      <ThumbsDown className="w-3.5 h-3.5" />
                      <span>Dispute ({item.downvotes})</span>
                    </button>
                  </div>

                  <span className="text-[11px] text-slate-500">
                    {item.userVote ? `You voted: ${item.userVote.toUpperCase()}` : 'One vote per user'}
                  </span>
                </div>
              </Card>
            </ThreeDCard>
          );
        })}
      </div>
    </div>
  );
};
