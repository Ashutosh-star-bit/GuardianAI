import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ShieldCheck,
  ShieldAlert,
  MessageSquare,
  Mail,
  Globe,
  QrCode,
  ArrowRight,
  Sparkles,
  Lock,
  Eye,
  Check,
  Activity,
  Zap,
  Crown,
  History,
  BarChart3,
  FileText,
  Building2,
  LogIn,
  AlertTriangle,
  User,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { FadeIn } from '../components/common/FadeIn';
import { Button } from '../components/common/Button';
import { Card } from '../components/common/Card';
import { ScannerConsole } from '../components/ScannerConsole';
import { useAuth } from '../context/AuthContext';

import { ThreeDCard } from '../components/3d/ThreeDCard';
import { FloatingShield3D } from '../components/3d/FloatingShield3D';

export const HomePage: React.FC = () => {
  const { isAuthenticated, currentUser, effectiveTier, scanHistory } = useAuth();
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  const toggleFaq = (index: number) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  const faqData = [
    {
      q: 'How does GuardianAI protect my privacy while analyzing messages?',
      a: 'GuardianAI uses a Zero-Knowledge Privacy pipeline. All personal identifiers—such as credit card numbers, Social Security Numbers, phone numbers, and names—are scrubbed locally inside your browser using Web Workers before any payload is sent to our AI engines.',
    },
    {
      q: 'What is Explainable AI (XAI) and why is it better than traditional filters?',
      a: 'Traditional anti-spam filters act as "black boxes" that give you a vague pass/fail label without context. GuardianAI Explainable AI highlights exact manipulative phrases (fear, urgency, typosquatted links) and explains in plain language WHY a message is dangerous, empowering you to spot future scams.',
    },
    {
      q: 'What is Senior Citizen High-Contrast Mode?',
      a: 'Senior Mode is an accessible accessibility preset designed for older adults. Pressing Alt+S or clicking the Senior Mode button instantly activates a warm light background, 20px+ extra-large fonts, 12:1 contrast ratio, and replaces technical jargon with simple step-by-step guidance.',
    },
    {
      q: 'Can I use GuardianAI for free?',
      a: 'Yes! Our Free Tier gives you 15 AI scans per month across text messages, URLs, emails, and QR codes with full Zero-Knowledge privacy protection.',
    },
  ];

  // =========================================================================
  // A. AUTHENTICATED USER HOME DASHBOARD (When User is Signed In)
  // =========================================================================
  if (isAuthenticated && currentUser) {
    const totalScans = scanHistory.length;
    const dangerousCount = scanHistory.filter((s) => s.riskBand === 'dangerous').length;
    const scansUsed = currentUser.scanCount || 0;
    const limit = effectiveTier === 'FREE' ? 15 : 'Unlimited';

    return (
      <PageTransition className="space-y-8 py-4">
        {/* User Welcome Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-sky-950/40 to-slate-900 border border-sky-500/30 rounded-3xl p-6 sm:p-8 space-y-4 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="bg-sky-500/20 text-sky-400 border border-sky-500/40 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Threat Defense Active</span>
                </span>
                <span className="bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-full text-xs font-black uppercase flex items-center gap-1">
                  <Crown className="w-3.5 h-3.5 text-amber-400" />
                  <span>{effectiveTier} PLAN</span>
                </span>
              </div>

              <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
                Welcome Back, <span className="text-sky-400">{currentUser.fullName}</span>!
              </h1>
              <p className="text-xs sm:text-sm text-slate-300 max-w-xl">
                Your digital identity is guarded by Zero-Knowledge Explainable AI. Select an inspection engine below to analyze suspicious communications.
              </p>
            </div>

            {/* Monthly Allowance Pill */}
            <div className="bg-slate-950/90 border border-slate-800 p-4 rounded-2xl text-center shrink-0 min-w-[180px]">
              <div className="text-[11px] text-slate-400 font-bold uppercase">Monthly AI Scans</div>
              <div className="text-2xl font-black text-white font-mono mt-0.5">
                {scansUsed} / <span className="text-sky-400">{limit}</span>
              </div>
              <p className="text-[10px] text-slate-500 mt-1">
                {effectiveTier === 'FREE' ? `${15 - Math.min(15, scansUsed)} scans remaining` : 'Unlimited Plan Active'}
              </p>
            </div>
          </div>
        </div>

        {/* Quick Inspection Tool Launchers */}
        <div className="space-y-4">
          <h2 className="text-xl font-black text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-sky-400" />
            <span>Launch Inspection Engine</span>
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link to="/scan/message">
              <Card className="p-5 border-slate-800 hover:border-sky-500/60 bg-slate-900/90 hover:bg-slate-900 transition-all group h-full flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="p-3 bg-sky-500/10 border border-sky-500/30 rounded-2xl w-fit text-sky-400 group-hover:scale-110 transition-transform">
                    <MessageSquare className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base group-hover:text-sky-400 transition-colors">SMS Smishing</h3>
                    <p className="text-xs text-slate-400 mt-1">Inspect text messages, SMS urgency, & mobile bank traps.</p>
                  </div>
                </div>
                <div className="mt-4 text-xs font-bold text-sky-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  <span>Start SMS Inspection</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Card>
            </Link>

            <Link to="/scan/email">
              <Card className="p-5 border-slate-800 hover:border-blue-500/60 bg-slate-900/90 hover:bg-slate-900 transition-all group h-full flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-2xl w-fit text-blue-400 group-hover:scale-110 transition-transform">
                    <Mail className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base group-hover:text-blue-400 transition-colors">Email BEC</h3>
                    <p className="text-xs text-slate-400 mt-1">Verify SPF/DKIM headers, invoice fraud & CEO spoofing.</p>
                  </div>
                </div>
                <div className="mt-4 text-xs font-bold text-blue-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  <span>Inspect Email Header</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Card>
            </Link>

            <Link to="/scan/url">
              <Card className="p-5 border-slate-800 hover:border-emerald-500/60 bg-slate-900/90 hover:bg-slate-900 transition-all group h-full flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl w-fit text-emerald-400 group-hover:scale-110 transition-transform">
                    <Globe className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base group-hover:text-emerald-400 transition-colors">URL Typosquat</h3>
                    <p className="text-xs text-slate-400 mt-1">Detect homoglyph domain spoofs & zero-day WHOIS links.</p>
                  </div>
                </div>
                <div className="mt-4 text-xs font-bold text-emerald-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  <span>Verify Web Domain</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Card>
            </Link>

            <Link to="/scan/qr">
              <Card className="p-5 border-slate-800 hover:border-amber-500/60 bg-slate-900/90 hover:bg-slate-900 transition-all group h-full flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-2xl w-fit text-amber-400 group-hover:scale-110 transition-transform">
                    <QrCode className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base group-hover:text-amber-400 transition-colors">QR Quishing</h3>
                    <p className="text-xs text-slate-400 mt-1">Safely decode QR code flyers, parking meters & posters.</p>
                  </div>
                </div>
                <div className="mt-4 text-xs font-bold text-amber-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  <span>Decode QR Image</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Card>
            </Link>
          </div>
        </div>

        {/* Quick Telemetry & Shortcuts Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link to="/history" className="block">
            <Card className="p-5 border-slate-800 hover:border-slate-700 bg-slate-900/90 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 flex items-center gap-1.5">
                  <History className="w-4 h-4 text-sky-400" />
                  <span>Audit History</span>
                </span>
                <span className="text-sm font-black text-white font-mono">{totalScans} Scans</span>
              </div>
              <p className="text-xs text-slate-400">View real-time audit trail and export CSV telemetry reports.</p>
            </Card>
          </Link>

          <Link to="/community" className="block">
            <Card className="p-5 border-slate-800 hover:border-slate-700 bg-slate-900/90 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 flex items-center gap-1.5">
                  <ShieldAlert className="w-4 h-4 text-red-400" />
                  <span>Community Intel</span>
                </span>
                <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded font-bold uppercase">
                  Scammer Feed
                </span>
              </div>
              <p className="text-xs text-slate-400">Upvote and verify active scammer handles with the community.</p>
            </Card>
          </Link>

          <Link to="/reports" className="block">
            <Card className="p-5 border-slate-800 hover:border-slate-700 bg-slate-900/90 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 flex items-center gap-1.5">
                  <Building2 className="w-4 h-4 text-amber-400" />
                  <span>Government Reporting</span>
                </span>
                <span className="text-xs bg-amber-500/20 text-amber-400 px-2 py-0.5 rounded font-bold uppercase">
                  FTC / 1930
                </span>
              </div>
              <p className="text-xs text-slate-400">Export evidence packets and report threats to law enforcement.</p>
            </Card>
          </Link>
        </div>

        {/* Embedded Scanner Console */}
        <section className="space-y-4">
          <h2 className="text-xl font-black text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            <span>Instant Quick Scan Console</span>
          </h2>
          <ScannerConsole />
        </section>
      </PageTransition>
    );
  }

  // =========================================================================
  // B. PUBLIC MARKETING LANDING PAGE (When Visitor is Not Signed In)
  // =========================================================================
  return (
    <PageTransition className="space-y-24 py-6">
      {/* 1. HERO SECTION WITH 3D MASCOT */}
      <section className="relative max-w-6xl mx-auto pt-4 sm:pt-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] sm:w-[600px] h-[350px] sm:h-[600px] bg-gradient-to-tr from-sky-600/20 via-blue-600/10 to-transparent rounded-full blur-3xl pointer-events-none -z-10" />

        <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
          <FadeIn direction="down">
            <div className="inline-flex items-center gap-2 bg-slate-900/80 border border-sky-500/30 backdrop-blur-md text-sky-400 px-4 py-1.5 rounded-full text-xs sm:text-sm font-bold shadow-lg shadow-sky-500/10">
              <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
              <span>Next-Gen Explainable AI (XAI) Protection</span>
            </div>
          </FadeIn>

          <FadeIn delay={0.1}>
            <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-[1.1]">
              Detect Online Scams. <br />
              <span className="bg-gradient-to-r from-sky-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
                Understand Why. Stay Safe.
              </span>
            </h1>
          </FadeIn>

          <FadeIn delay={0.2}>
            <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
              GuardianAI inspects suspicious messages, emails, URLs, and QR codes—highlighting manipulative tactics in plain English while protecting your privacy.
            </p>
          </FadeIn>

          <FadeIn delay={0.3}>
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2">
              <a href="#scanner-console">
                <Button size="lg" className="shadow-sky-500/25 shadow-xl" rightIcon={<ArrowRight className="w-5 h-5" />}>
                  Start Free Scan
                </Button>
              </a>
              <Link to="/login">
                <Button variant="secondary" size="lg" leftIcon={<LogIn className="w-4 h-4" />}>
                  Sign In / Login
                </Button>
              </Link>
            </div>
          </FadeIn>

          <FadeIn delay={0.4}>
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 pt-4 text-xs text-slate-400 font-medium">
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Zero-Knowledge Privacy</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-amber-400" />
                <span>Sub-1.8s Response SLA</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Eye className="w-4 h-4 text-sky-400" />
                <span>Senior Citizen Friendly</span>
              </div>
            </div>
          </FadeIn>
        </div>

        {/* 3D FLOATING SHIELD MASCOT */}
        <div className="lg:col-span-5 flex justify-center">
          <FadeIn delay={0.25} direction="up">
            <FloatingShield3D />
          </FadeIn>
        </div>
      </section>

      {/* 2. DEMO PREVIEW (LIVE SCANNER CONSOLE) */}
      <section id="scanner-console" className="scroll-mt-24">
        <FadeIn>
          <div className="text-center space-y-2 mb-6">
            <h2 className="text-2xl sm:text-3xl font-black text-white">Try the Scanner Live</h2>
            <p className="text-sm text-slate-400">Paste any text payload below to test GuardianAI Explainable AI in real-time.</p>
          </div>
          <ScannerConsole />
        </FadeIn>
      </section>

      {/* 3. FEATURE CARDS GRID */}
      <section className="space-y-8">
        <div className="text-center space-y-3 max-w-2xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight">Complete Threat Protection</h2>
          <p className="text-base text-slate-400">Comprehensive AI inspection across all major attack vectors targeting individuals and businesses.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FadeIn delay={0.1}>
            <Card className="h-full hover:border-sky-500/50 transition-all duration-300 group">
              <div className="bg-sky-500/10 p-3 rounded-xl border border-sky-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <MessageSquare className="w-6 h-6 text-sky-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Message & SMS Smishing</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Detects artificial urgency, fear tactics, impersonation of banks, and UPI/Zelle money transfer scams.
              </p>
            </Card>
          </FadeIn>

          <FadeIn delay={0.2}>
            <Card className="h-full hover:border-blue-500/50 transition-all duration-300 group">
              <div className="bg-blue-500/10 p-3 rounded-xl border border-blue-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <Mail className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Email Header & BEC</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Parses SPF, DKIM, and DMARC authentication records to stop executive impersonation and fake invoice fraud.
              </p>
            </Card>
          </FadeIn>

          <FadeIn delay={0.3}>
            <Card className="h-full hover:border-emerald-500/50 transition-all duration-300 group">
              <div className="bg-emerald-500/10 p-3 rounded-xl border border-emerald-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <Globe className="w-6 h-6 text-emerald-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">URL & Typosquatting</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Flags homoglyph domain spoofs, zero-day WHOIS registrations, and malicious redirect chains.
              </p>
            </Card>
          </FadeIn>

          <FadeIn delay={0.4}>
            <Card className="h-full hover:border-amber-500/50 transition-all duration-300 group">
              <div className="bg-amber-500/10 p-3 rounded-xl border border-amber-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <QrCode className="w-6 h-6 text-amber-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Quishing (QR Code Fraud)</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Decodes parking meter and flyer QR codes safely without opening the destination link automatically.
              </p>
            </Card>
          </FadeIn>

          <FadeIn delay={0.5}>
            <Card className="h-full hover:border-indigo-500/50 transition-all duration-300 group">
              <div className="bg-indigo-500/10 p-3 rounded-xl border border-indigo-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <Lock className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Edge PII Anonymization</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Client-side Web Worker scrubs credit cards, SSNs, and phone numbers locally before AI inspection.
              </p>
            </Card>
          </FadeIn>

          <FadeIn delay={0.6}>
            <Card className="h-full hover:border-purple-500/50 transition-all duration-300 group">
              <div className="bg-purple-500/10 p-3 rounded-xl border border-purple-500/30 w-fit mb-4 group-hover:scale-110 transition-transform">
                <Eye className="w-6 h-6 text-purple-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Senior Mode AAA Accessibility</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                One-click toggle activates 20px+ font size, 12:1 warm contrast ratio, and zero jargon for senior citizens.
              </p>
            </Card>
          </FadeIn>
        </div>
      </section>

      {/* 4. BLACK-BOX VS EXPLAINABLE AI */}
      <section className="space-y-8">
        <div className="text-center space-y-3 max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-sky-500/10 border border-sky-500/30 text-sky-400 px-3 py-1 rounded-full text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Human-Centric Security Psychology</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight">Black-Box vs Explainable AI</h2>
          <p className="text-sm text-slate-400">
            Traditional spam filters give opaque labels that leave users confused. GuardianAI explains exact manipulative tactics so users recognize future threats.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-red-900/40 bg-red-950/20 space-y-4 p-6">
            <div className="flex items-center justify-between border-b border-red-900/30 pb-3">
              <h3 className="font-bold text-red-400 flex items-center gap-2 text-base">
                <ShieldAlert className="w-5 h-5" />
                <span>Opaque Legacy Filter (Black-Box)</span>
              </h3>
              <span className="text-xs text-red-400 font-mono bg-red-950 px-2.5 py-1 rounded-full border border-red-800 font-bold">
                0% Rationale
              </span>
            </div>
            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-3">
              <div className="text-xs font-mono text-slate-400 flex justify-between">
                <span>Filter Response:</span>
                <span className="text-red-400 font-bold">FLAGGED AS SPAM (Score: 88%)</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed bg-slate-900 p-3 rounded-xl">
                "Message blocked by rule #8491. No further explanation provided."
              </p>
              <div className="text-[11px] text-red-300/80 pt-1 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-red-400 shrink-0" />
                <span>User psychological impact: 74% of users re-click flagged links out of anxiety because they don't understand the risk.</span>
              </div>
            </div>
          </Card>

          <Card className="border-emerald-900/40 bg-emerald-950/20 space-y-4 p-6">
            <div className="flex items-center justify-between border-b border-emerald-900/30 pb-3">
              <h3 className="font-bold text-emerald-400 flex items-center gap-2 text-base">
                <ShieldCheck className="w-5 h-5" />
                <span>GuardianAI Explainable AI (XAI)</span>
              </h3>
              <span className="text-xs text-emerald-400 font-mono bg-emerald-950 px-2.5 py-1 rounded-full border border-emerald-800 font-bold">
                100% Transparent
              </span>
            </div>
            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-800/80 space-y-3">
              <div className="text-xs font-mono text-slate-400 flex justify-between">
                <span>XAI Analysis:</span>
                <span className="text-red-400 font-bold">DANGEROUS SCAM (88/100)</span>
              </div>
              <p className="text-xs text-slate-200 bg-slate-900 p-3 rounded-xl leading-relaxed">
                <span className="bg-red-500/20 text-red-300 font-bold px-1 rounded">URGENT:</span> Your bank account is locked. Verify at <span className="bg-amber-500/20 text-amber-300 font-bold px-1 rounded">http://paypa1-check.com</span> immediately.
              </p>
              <div className="text-xs text-slate-300 bg-slate-900/90 p-3 rounded-xl border border-sky-500/30 space-y-1">
                <strong className="text-sky-400 block font-bold">Plain-English Rationale:</strong>
                <p className="text-[11px] text-slate-300 leading-normal">
                  1. Artificial Urgency trigger ("URGENT", "immediately") forces rapid action.<br />
                  2. Typosquatted link ("paypa1-check.com") spoofs PayPal using character substitution ('1' for 'l').
                </p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* 5. PRICING SECTION */}
      <section className="space-y-8">
        <div className="text-center space-y-3 max-w-2xl mx-auto">
          <h2 className="text-3xl font-black text-white tracking-tight">Flexible Protection Plans</h2>
          <p className="text-sm text-slate-400">Choose the plan that fits your personal or organizational safety needs.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">Free Tier</h3>
              <p className="text-3xl font-black text-white">$0 / ₹0 <span className="text-xs text-slate-400 font-normal">/ month forever</span></p>
              <ul className="space-y-2 text-xs text-slate-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400 shrink-0" /> 15 Scans / Month</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400 shrink-0" /> SMS & Text Message Inspector</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400 shrink-0" /> URL & Typosquatting Checker</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400 shrink-0" /> Senior Mode Accessibility</li>
              </ul>
            </div>
            <Link to="/register">
              <Button variant="secondary" className="w-full">Get Started Free</Button>
            </Link>
          </Card>

          <Card className="flex flex-col justify-between space-y-6 border-sky-500/80 shadow-sky-glow relative">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-sky-600 text-white text-[10px] uppercase font-bold px-3 py-1 rounded-full border border-sky-400">
              Most Popular
            </div>
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">Pro Personal</h3>
              <p className="text-3xl font-black text-white">$4.99 / ₹399 <span className="text-xs text-slate-400 font-normal">/ month</span></p>
              <ul className="space-y-2 text-xs text-slate-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-sky-400 shrink-0" /> Unlimited AI Scans</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-sky-400 shrink-0" /> Email Header BEC Scanner</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-sky-400 shrink-0" /> Quishing QR Scanner</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-sky-400 shrink-0" /> Priority Fast-Queue AI</li>
              </ul>
            </div>
            <Link to="/login">
              <Button className="w-full">Start 14-Day Free Trial</Button>
            </Link>
          </Card>

          <Card className="flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">Business SMB</h3>
              <p className="text-3xl font-black text-white">$14.99 / ₹1,199 <span className="text-xs text-slate-400 font-normal">/ month</span></p>
              <ul className="space-y-2 text-xs text-slate-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-indigo-400 shrink-0" /> Everything in Pro</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-indigo-400 shrink-0" /> Team Threat Dashboard</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-indigo-400 shrink-0" /> Developer API Access</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-indigo-400 shrink-0" /> 1-Click FTC Fraud Reporting</li>
              </ul>
            </div>
            <Link to="/login">
              <Button variant="secondary" className="w-full">Contact Sales</Button>
            </Link>
          </Card>
        </div>
      </section>

      {/* 6. FAQ ACCORDION SECTION */}
      <section className="space-y-8 max-w-3xl mx-auto">
        <div className="text-center space-y-3">
          <h2 className="text-3xl font-black text-white tracking-tight">Frequently Asked Questions</h2>
          <p className="text-sm text-slate-400">Everything you need to know about GuardianAI protection.</p>
        </div>

        <div className="space-y-4">
          {faqData.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <div key={idx} className="cursor-pointer" onClick={() => toggleFaq(idx)}>
                <Card className="p-4 border-slate-800 bg-slate-900/90">
                  <div className="flex items-center justify-between font-bold text-sm text-white">
                    <span>{faq.q}</span>
                    <span className="text-sky-400 font-mono text-base">{isOpen ? '−' : '+'}</span>
                  </div>
                  {isOpen && <p className="text-xs text-slate-300 mt-2 leading-relaxed pt-2 border-t border-slate-800/60">{faq.a}</p>}
                </Card>
              </div>
            );
          })}
        </div>
      </section>
    </PageTransition>
  );
};
