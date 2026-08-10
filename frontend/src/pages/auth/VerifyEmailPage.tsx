import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Mail, Phone, RotateCw, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';

export const VerifyEmailPage: React.FC = () => {
  const {
    pendingEmail,
    pendingPhone,
    emailVerified,
    phoneVerified,
    sendPhoneOtp,
    verifyPhoneOtp,
    resendEmailVerification,
    checkEmailVerified,
    finalizeRegistration,
  } = useAuth();

  const [smsCode, setSmsCode] = useState(['', '', '', '', '', '']);
  const [isVerifyingPhone, setIsVerifyingPhone] = useState(false);
  const [isSmsSent, setIsSmsSent] = useState(false);
  const [isSendingSms, setIsSendingSms] = useState(false);
  const [isResendingEmail, setIsResendingEmail] = useState(false);
  const [emailCheckCount, setEmailCheckCount] = useState(0);
  const { showToast } = useToast();
  const navigate = useNavigate();
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Poll for email verification every 3 seconds
  useEffect(() => {
    if (emailVerified) return;

    pollingRef.current = setInterval(async () => {
      const verified = await checkEmailVerified();
      setEmailCheckCount((c) => c + 1);
      if (verified) {
        showToast('success', 'Email Verified!', 'Your email address has been verified successfully.');
        if (pollingRef.current) clearInterval(pollingRef.current);
      }
    }, 3000);

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [emailVerified, checkEmailVerified, showToast]);

  // Auto-finalize when both are verified
  useEffect(() => {
    if (emailVerified && phoneVerified) {
      showToast('success', 'Dual Verification Complete!', 'Both email and phone verified. Welcome to GuardianAI!');
      finalizeRegistration();
      navigate('/dashboard');
    }
  }, [emailVerified, phoneVerified, finalizeRegistration, navigate, showToast]);

  const handleSmsCodeChange = (index: number, value: string) => {
    if (value.length > 1) return;
    const newCode = [...smsCode];
    newCode[index] = value;
    setSmsCode(newCode);

    if (value && index < 5) {
      const nextInput = document.getElementById(`sms-code-input-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleSendSms = async () => {
    if (!pendingPhone) return;
    setIsSendingSms(true);

    const result = await sendPhoneOtp(pendingPhone, 'recaptcha-container');
    setIsSendingSms(false);

    if (result.success) {
      setIsSmsSent(true);
      showToast('success', 'SMS Sent!', result.message);
    } else {
      showToast('error', 'SMS Failed', result.message);
    }
  };

  const handleVerifyPhone = async () => {
    const fullCode = smsCode.join('');
    if (fullCode.length < 6) {
      showToast('error', 'Incomplete Code', 'Please enter all 6 digits of your SMS code.');
      return;
    }

    setIsVerifyingPhone(true);
    const result = await verifyPhoneOtp(fullCode);
    setIsVerifyingPhone(false);

    if (result.success) {
      showToast('success', 'Phone Verified!', result.message);
    } else {
      showToast('error', 'Verification Failed', result.message);
    }
  };

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
          <h1 className="text-3xl font-black text-white tracking-tight">Verify Your Account</h1>
          <p className="text-sm text-slate-400">
            Complete both verification steps to activate your GuardianAI account.
          </p>
        </div>

        {/* ── STEP 1: EMAIL VERIFICATION ────────────────────── */}
        <Card className="space-y-4 border-slate-800 bg-slate-900/90">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            {emailVerified ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            ) : (
              <Mail className="w-5 h-5 text-sky-400" />
            )}
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Step 1: Email Verification
            </h2>
            {emailVerified && (
              <span className="ml-auto text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                ✓ VERIFIED
              </span>
            )}
          </div>

          {emailVerified ? (
            <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-4 text-center">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
              <p className="text-sm text-emerald-300 font-bold">Email verified successfully!</p>
              <p className="text-xs text-slate-400 mt-1">{pendingEmail}</p>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="bg-sky-950/40 border border-sky-500/20 rounded-xl p-4 text-center space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <Loader2 className="w-4 h-4 text-sky-400 animate-spin" />
                  <span className="text-xs font-bold text-sky-300 uppercase tracking-wider">
                    Waiting for email verification...
                  </span>
                </div>
                <p className="text-sm text-white">
                  We sent a verification link to <strong className="text-sky-300">{pendingEmail || 'your email'}</strong>
                </p>
                <p className="text-xs text-slate-400">
                  Open your Gmail inbox, find the email from <strong>noreply@guardianai-f6be8.firebaseapp.com</strong>, and click the verification link.
                </p>
                <div className="text-[11px] text-amber-300/90 flex items-center justify-center gap-1.5 font-medium pt-1">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                  <span>Check your <strong className="text-amber-200">Spam / Junk</strong> folder if you don't see it in your inbox.</span>
                </div>
              </div>

              <button
                onClick={handleResendEmail}
                disabled={isResendingEmail}
                className="w-full py-2 text-xs text-slate-400 hover:text-sky-400 font-bold transition-colors inline-flex items-center justify-center gap-1.5 disabled:opacity-50"
              >
                <RotateCw className={`w-3.5 h-3.5 ${isResendingEmail ? 'animate-spin' : ''}`} />
                <span>{isResendingEmail ? 'Resending...' : 'Resend Verification Email'}</span>
              </button>

              {emailCheckCount > 10 && (
                <p className="text-[11px] text-slate-500 text-center">
                  Still checking... This page auto-detects when you click the email link.
                </p>
              )}
            </div>
          )}
        </Card>

        {/* ── STEP 2: PHONE SMS VERIFICATION ────────────────── */}
        {pendingPhone && (
          <Card className="space-y-4 border-slate-800 bg-slate-900/90">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              {phoneVerified ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              ) : (
                <Phone className="w-5 h-5 text-emerald-400" />
              )}
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">
                Step 2: Phone SMS Verification
              </h2>
              {phoneVerified && (
                <span className="ml-auto text-[10px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                  ✓ VERIFIED
                </span>
              )}
            </div>

            {phoneVerified ? (
              <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-4 text-center">
                <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
                <p className="text-sm text-emerald-300 font-bold">Phone number verified!</p>
                <p className="text-xs text-slate-400 mt-1">{pendingPhone}</p>
              </div>
            ) : !isSmsSent ? (
              <div className="space-y-3 text-center">
                <p className="text-sm text-slate-300">
                  Send a real 6-digit SMS code to <strong className="text-white">{pendingPhone}</strong>
                </p>
                <Button
                  onClick={handleSendSms}
                  disabled={isSendingSms}
                  className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-sm"
                >
                  {isSendingSms ? 'Sending SMS...' : 'Send SMS Verification Code'}
                </Button>
                <p className="text-[11px] text-slate-500">
                  Phone number must be in international format: +91XXXXXXXXXX
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <p className="text-sm text-slate-300 text-center">
                  Enter the 6-digit code sent to <strong className="text-white">{pendingPhone}</strong>
                </p>

                <div className="flex justify-center gap-2">
                  {smsCode.map((digit, idx) => (
                    <input
                      key={idx}
                      id={`sms-code-input-${idx}`}
                      type="text"
                      inputMode="numeric"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleSmsCodeChange(idx, e.target.value.replace(/\D/g, ''))}
                      className="w-11 h-12 text-center text-xl font-bold bg-slate-950 border border-slate-800 focus:border-emerald-400 text-white rounded-xl outline-none transition-all"
                    />
                  ))}
                </div>

                <Button
                  onClick={handleVerifyPhone}
                  disabled={isVerifyingPhone}
                  className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-sm"
                >
                  {isVerifyingPhone ? 'Verifying...' : 'Verify Phone Number'}
                </Button>

                <button
                  onClick={handleSendSms}
                  disabled={isSendingSms}
                  className="w-full py-2 text-xs text-slate-400 hover:text-emerald-400 font-bold transition-colors inline-flex items-center justify-center gap-1.5 disabled:opacity-50"
                >
                  <RotateCw className={`w-3.5 h-3.5 ${isSendingSms ? 'animate-spin' : ''}`} />
                  <span>{isSendingSms ? 'Resending...' : 'Resend SMS Code'}</span>
                </button>
              </div>
            )}
          </Card>
        )}

        {/* Invisible reCAPTCHA container for Firebase Phone Auth */}
        <div id="recaptcha-container" />
      </div>
    </PageTransition>
  );
};
