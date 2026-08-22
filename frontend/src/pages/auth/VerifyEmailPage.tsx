import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Mail, RotateCw, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';

export const VerifyEmailPage: React.FC = () => {
  const {
    pendingEmail,
    emailVerified,
    resendEmailVerification,
    checkEmailVerified,
    finalizeRegistration,
  } = useAuth();

  const [isResendingEmail, setIsResendingEmail] = useState(false);
  const [emailCheckCount, setEmailCheckCount] = useState(0);
  const { showToast } = useToast();
  const navigate = useNavigate();
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const hasFinalized = useRef(false);

  // Poll for email verification every 3 seconds
  useEffect(() => {
    if (emailVerified || hasFinalized.current) return;

    pollingRef.current = setInterval(async () => {
      const verified = await checkEmailVerified();
      setEmailCheckCount((c) => c + 1);
      if (verified && !hasFinalized.current) {
        hasFinalized.current = true;
        if (pollingRef.current) clearInterval(pollingRef.current);
        showToast('success', 'Email Verified!', 'Your email has been verified. Welcome to GuardianAI!');
        finalizeRegistration();
        navigate('/dashboard');
      }
    }, 3000);

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [emailVerified, checkEmailVerified, finalizeRegistration, navigate, showToast]);

  const handleResendEmail = async () => {
    setIsResendingEmail(true);
    const result = await resendEmailVerification();
    setIsResendingEmail(false);

    if (result.success) {
      showToast('info', 'Email Resent', result.message);
    } else {
      showToast('error', 'Resend Failed', result.message);
    }
  };

  return (
    <PageTransition className="min-h-[85vh] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-lg space-y-6">
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2">
            <div className="bg-sky-500/10 p-2.5 rounded-2xl border border-sky-500/30">
              <ShieldCheck className="w-8 h-8 text-sky-400" />
            </div>
          </Link>
          <h1 className="text-3xl font-black text-white tracking-tight">Verify Your Email</h1>
          <p className="text-sm text-slate-400">
            Click the verification link sent to your email inbox to activate your account.
          </p>
        </div>

        <Card className="space-y-5 border-slate-800 bg-slate-900/90">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            {emailVerified ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            ) : (
              <Mail className="w-5 h-5 text-sky-400" />
            )}
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Email Verification
            </h2>
            {emailVerified && (
              <span className="ml-auto text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                ✓ VERIFIED
              </span>
            )}
          </div>

          {emailVerified ? (
            <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-6 text-center">
              <CheckCircle2 className="w-10 h-10 text-emerald-400 mx-auto mb-3" />
              <p className="text-base text-emerald-300 font-bold">Email verified successfully!</p>
              <p className="text-xs text-slate-400 mt-1">Redirecting to dashboard...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Animated waiting state */}
              <div className="bg-sky-950/40 border border-sky-500/20 rounded-xl p-5 text-center space-y-3">
                <div className="w-16 h-16 mx-auto rounded-full bg-sky-500/10 border border-sky-500/30 flex items-center justify-center">
                  <Loader2 className="w-8 h-8 text-sky-400 animate-spin" />
                </div>

                <div>
                  <p className="text-xs font-bold text-sky-300 uppercase tracking-wider mb-1">
                    Waiting for email verification...
                  </p>
                  <p className="text-sm text-white">
                    We sent a verification link to:
                  </p>
                  <p className="text-base font-bold text-sky-300 mt-1">
                    {pendingEmail || 'your email'}
                  </p>
                </div>

                <div className="bg-slate-950 rounded-lg p-3 text-left space-y-2 text-xs text-slate-300">
                  <p className="font-bold text-white text-sm">📧 What to do:</p>
                  <ol className="list-decimal list-inside space-y-1">
                    <li>Open your <strong className="text-white">email inbox</strong></li>
                    <li>Find the email from <strong className="text-sky-300">noreply@guardianai-f6be8.firebaseapp.com</strong></li>
                    <li>Click the <strong className="text-white">verification link</strong> in the email</li>
                    <li>This page will <strong className="text-emerald-300">automatically detect</strong> the verification</li>
                  </ol>
                </div>

                <div className="text-[11px] text-amber-300/90 flex items-center justify-center gap-1.5 font-medium pt-1">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                  <span>Check your <strong className="text-amber-200">Spam / Junk</strong> folder if you don't see the email.</span>
                </div>
              </div>

              {/* Resend button */}
              <button
                onClick={handleResendEmail}
                disabled={isResendingEmail}
                className="w-full py-2.5 text-xs text-slate-400 hover:text-sky-400 font-bold transition-colors inline-flex items-center justify-center gap-1.5 disabled:opacity-50 border border-slate-800 rounded-xl hover:border-sky-500/30"
              >
                <RotateCw className={`w-3.5 h-3.5 ${isResendingEmail ? 'animate-spin' : ''}`} />
                <span>{isResendingEmail ? 'Resending...' : 'Resend Verification Email'}</span>
              </button>

              {emailCheckCount > 10 && (
                <p className="text-[11px] text-slate-500 text-center">
                  Still checking... (checked {emailCheckCount} times). This page auto-detects when you click the email link.
                </p>
              )}
            </div>
          )}
        </Card>
      </div>
    </PageTransition>
  );
};
