import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Mail, RotateCw, AlertCircle, Eye, EyeOff, Sparkles } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';

export const VerifyEmailPage: React.FC = () => {
  const { pendingEmail, verificationOtp, verifyOtpCode, resendVerificationCode } = useAuth();
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [isVerifying, setIsVerifying] = useState(false);
  const [showHelperCode, setShowHelperCode] = useState(false);
  const { showToast } = useToast();
  const navigate = useNavigate();

  const handleCodeChange = (index: number, value: string) => {
    if (value.length > 1) return;
    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);

    // Auto-focus next input field
    if (value && index < 5) {
      const nextInput = document.getElementById(`code-input-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleVerify = async () => {
    const fullCode = code.join('');
    if (fullCode.length < 6) {
      showToast('error', 'Incomplete Code', 'Please enter all 6 digits of your verification code.');
      return;
    }

    setIsVerifying(true);
    setTimeout(() => {
      const isValid = verifyOtpCode(fullCode);
      setIsVerifying(false);

      if (isValid) {
        showToast('success', 'Email Verified!', 'Your account has been fully activated. Welcome to GuardianAI!');
        navigate('/dashboard');
      } else {
        showToast('error', 'Verification Failed', 'Invalid 6-digit code. Please enter the exact verification code sent to your email.');
      }
    }, 800);
  };

  const handleResend = async () => {
    const res = await resendVerificationCode();
    if (res.success) {
      showToast('info', 'Code Resent!', `A new 6-digit code has been dispatched to ${pendingEmail || 'your email'}.`);
      setCode(['', '', '', '', '', '']);
    } else {
      showToast('error', 'Error', 'Unable to resend verification code.');
    }
  };

  const handleAutoFillCode = () => {
    if (verificationOtp && verificationOtp.length === 6) {
      const digits = verificationOtp.split('');
      setCode(digits);
      showToast('success', 'Code Auto-Filled!', 'Verification code filled automatically.');
    }
  };

  return (
    <PageTransition className="min-h-[80vh] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2">
            <div className="bg-sky-500/10 p-2.5 rounded-2xl border border-sky-500/30">
              <ShieldCheck className="w-8 h-8 text-sky-400" />
            </div>
          </Link>
          <h1 className="text-3xl font-black text-white tracking-tight">Verify Your Email</h1>
          <p className="text-sm text-slate-400">
            Enter the 6-digit verification code sent to <strong className="text-white">{pendingEmail || 'your email'}</strong>
          </p>
        </div>

        {/* Security Email Dispatch Info Banner */}
        <div className="bg-sky-950/40 border border-sky-500/30 rounded-2xl p-4 text-center space-y-2.5">
          <div className="flex items-center justify-center gap-1.5 text-xs font-bold text-sky-300 uppercase tracking-wider">
            <Mail className="w-4 h-4 text-sky-400" />
            <span>Verification Email Dispatched</span>
          </div>
          <p className="text-xs text-slate-300">
            A 6-digit verification code was sent to <strong className="text-white">{pendingEmail || 'your email inbox'}</strong>.
          </p>
          
          <div className="pt-2 border-t border-sky-500/20 space-y-2">
            <div className="text-[11px] text-amber-300/90 flex items-center justify-center gap-1.5 font-medium">
              <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span>Please check your <strong className="text-amber-200">Spam / Junk</strong> folder if not in primary inbox.</span>
            </div>

            {/* Revealer / Auto-fill Helper for Testing */}
            {verificationOtp && (
              <div className="pt-1 flex items-center justify-center gap-2">
                <button
                  type="button"
                  onClick={() => setShowHelperCode(!showHelperCode)}
                  className="text-xs text-sky-400 hover:text-sky-300 font-bold underline flex items-center gap-1 transition-colors"
                >
                  {showHelperCode ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  <span>{showHelperCode ? 'Hide Testing Helper Code' : 'Click to View Testing Code'}</span>
                </button>

                {showHelperCode && (
                  <button
                    type="button"
                    onClick={handleAutoFillCode}
                    className="px-2 py-0.5 bg-sky-500/20 border border-sky-400/40 text-sky-300 text-[11px] font-bold rounded-lg hover:bg-sky-500/30 flex items-center gap-1"
                  >
                    <Sparkles className="w-3 h-3 text-sky-400" />
                    <span>Auto-Fill [{verificationOtp}]</span>
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        <Card className="space-y-6 border-slate-800 bg-slate-900/90">
          <div className="space-y-4">
            <label className="text-xs font-bold text-slate-300 block text-center">
              6-Digit Verification Code
            </label>

            <div className="flex justify-center gap-2">
              {code.map((digit, idx) => (
                <input
                  key={idx}
                  id={`code-input-${idx}`}
                  type="text"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleCodeChange(idx, e.target.value)}
                  className="w-11 h-12 text-center text-xl font-bold bg-slate-950 border border-slate-800 focus:border-sky-400 text-white rounded-xl outline-none transition-all"
                />
              ))}
            </div>
          </div>

          <Button
            onClick={handleVerify}
            disabled={isVerifying}
            className="w-full py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black rounded-xl text-sm"
          >
            {isVerifying ? 'Verifying Code...' : 'Complete Account Activation'}
          </Button>

          <div className="text-center pt-2">
            <button
              onClick={handleResend}
              className="text-xs text-slate-400 hover:text-sky-400 font-bold transition-colors inline-flex items-center gap-1.5"
            >
              <RotateCw className="w-3.5 h-3.5" />
              <span>Didn't receive code? Resend Email</span>
            </button>
          </div>
        </Card>
      </div>
    </PageTransition>
  );
};
