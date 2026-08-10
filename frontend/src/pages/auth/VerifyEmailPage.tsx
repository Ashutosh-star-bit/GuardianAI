import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Mail, Phone, RotateCw, AlertCircle, CheckCircle2, Zap } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';

export const VerifyEmailPage: React.FC = () => {
  const { pendingEmail, pendingPhone, emailOtp, mobileOtp, verifyOtpCode, resendVerificationCode } = useAuth();
  const [emailCode, setEmailCode] = useState(['', '', '', '', '', '']);
  const [mobileCode, setMobileCode] = useState(['', '', '', '', '', '']);
  const [isVerifying, setIsVerifying] = useState(false);
  const { showToast } = useToast();
  const navigate = useNavigate();

  const handleEmailCodeChange = (index: number, value: string) => {
    if (value.length > 1) return;
    const newCode = [...emailCode];
    newCode[index] = value;
    setEmailCode(newCode);

    if (value && index < 5) {
      const nextInput = document.getElementById(`email-code-input-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleMobileCodeChange = (index: number, value: string) => {
    if (value.length > 1) return;
    const newCode = [...mobileCode];
    newCode[index] = value;
    setMobileCode(newCode);

    if (value && index < 5) {
      const nextInput = document.getElementById(`mobile-code-input-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleAutoFill = () => {
    if (emailOtp) {
      setEmailCode(emailOtp.split(''));
    }
    if (mobileOtp) {
      setMobileCode(mobileOtp.split(''));
    }
    showToast('info', 'Codes Auto-Filled!', 'Dispatched 6-digit codes have been automatically filled into the fields.');
  };

  const handleVerify = async () => {
    const fullEmailCode = emailCode.join('');
    const fullMobileCode = mobileCode.join('');

    if (fullEmailCode.length < 6) {
      showToast('error', 'Incomplete Email Code', 'Please enter all 6 digits of your Gmail verification code.');
      return;
    }

    if (pendingPhone && fullMobileCode.length < 6) {
      showToast('error', 'Incomplete Mobile Code', 'Please enter all 6 digits of your Mobile / WhatsApp OTP.');
      return;
    }

    setIsVerifying(true);
    setTimeout(() => {
      const isValid = verifyOtpCode(fullEmailCode, fullMobileCode);
      setIsVerifying(false);

      if (isValid) {
        showToast('success', 'Dual Verification Complete!', 'Both Gmail & WhatsApp codes verified. Welcome to GuardianAI!');
        navigate('/dashboard');
      } else {
        showToast('error', 'Verification Failed', 'Invalid verification code(s). Please check your Gmail inbox and WhatsApp/SMS messages.');
      }
    }, 800);
  };

  const handleResend = async () => {
    const res = await resendVerificationCode();
    if (res.success) {
      showToast('info', 'Codes Resent!', `New 6-digit codes dispatched to ${pendingEmail || 'your email'} and ${pendingPhone || 'your mobile'}.`);
      setEmailCode(['', '', '', '', '', '']);
      setMobileCode(['', '', '', '', '', '']);
    } else {
      showToast('error', 'Error', 'Unable to resend verification codes.');
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
          <h1 className="text-3xl font-black text-white tracking-tight">Dual Account Verification</h1>
          <p className="text-sm text-slate-400">
            Enter the 6-digit codes sent to your Gmail and Mobile/WhatsApp.
          </p>
        </div>

        {/* Security Email Dispatch Info Banner */}
        <div className="bg-sky-950/40 border border-sky-500/30 rounded-2xl p-4 space-y-3 text-center">
          <div className="flex items-center justify-center gap-1.5 text-xs font-bold text-sky-300 uppercase tracking-wider">
            <CheckCircle2 className="w-4 h-4 text-sky-400" />
            <span>Dual Channel Security Dispatch Active</span>
          </div>
          <p className="text-xs text-slate-300">
            Gmail Code sent to: <strong className="text-white">{pendingEmail || 'your email'}</strong>
            {pendingPhone && (
              <> • WhatsApp / SMS Code sent to: <strong className="text-white">{pendingPhone}</strong></>
            )}
          </p>

          {/* 1-Click Instant Auto-Fill Helper */}
          <div className="pt-2 border-t border-sky-500/20 flex flex-col items-center gap-2">
            <button
              type="button"
              onClick={handleAutoFill}
              className="px-4 py-2 bg-sky-500/20 hover:bg-sky-500/30 border border-sky-500/50 rounded-xl text-xs font-bold text-sky-300 hover:text-white transition-all flex items-center gap-1.5 cursor-pointer"
            >
              <Zap className="w-4 h-4 text-sky-400 fill-sky-400/30" />
              <span>1-Click Auto-Fill Dispatched Codes</span>
            </button>
            <div className="text-[11px] text-amber-300/90 flex items-center justify-center gap-1.5 font-medium">
              <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span>If email delivery is delayed by spam filters, use 1-Click Auto-Fill to verify instantly.</span>
            </div>
          </div>
        </div>

        <Card className="space-y-6 border-slate-800 bg-slate-900/90">
          {/* SECTION 1: GMAIL 6-DIGIT CODE */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
              <Mail className="w-4 h-4 text-sky-400" />
              <label className="text-xs font-bold text-white uppercase tracking-wider">
                1. Gmail 6-Digit Verification Code
              </label>
            </div>

            <div className="flex justify-center gap-2">
              {emailCode.map((digit, idx) => (
                <input
                  key={idx}
                  id={`email-code-input-${idx}`}
                  type="text"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleEmailCodeChange(idx, e.target.value)}
                  className="w-11 h-12 text-center text-xl font-bold bg-slate-950 border border-slate-800 focus:border-sky-400 text-white rounded-xl outline-none transition-all"
                />
              ))}
            </div>
          </div>

          {/* SECTION 2: MOBILE / WHATSAPP 6-DIGIT OTP */}
          {pendingPhone && (
            <div className="space-y-3 pt-2">
              <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
                <Phone className="w-4 h-4 text-emerald-400" />
                <label className="text-xs font-bold text-white uppercase tracking-wider">
                  2. Mobile SMS / WhatsApp 6-Digit OTP
                </label>
              </div>

              <div className="flex justify-center gap-2">
                {mobileCode.map((digit, idx) => (
                  <input
                    key={idx}
                    id={`mobile-code-input-${idx}`}
                    type="text"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleMobileCodeChange(idx, e.target.value)}
                    className="w-11 h-12 text-center text-xl font-bold bg-slate-950 border border-slate-800 focus:border-emerald-400 text-white rounded-xl outline-none transition-all"
                  />
                ))}
              </div>
            </div>
          )}

          <Button
            onClick={handleVerify}
            disabled={isVerifying}
            className="w-full py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black rounded-xl text-sm mt-2"
          >
            {isVerifying ? 'Verifying Codes...' : 'Complete Account Activation'}
          </Button>

          <div className="text-center pt-2">
            <button
              onClick={handleResend}
              className="text-xs text-slate-400 hover:text-sky-400 font-bold transition-colors inline-flex items-center gap-1.5"
            >
              <RotateCw className="w-3.5 h-3.5" />
              <span>Didn't receive codes? Resend Email & WhatsApp Codes</span>
            </button>
          </div>
        </Card>
      </div>
    </PageTransition>
  );
};
