import React from 'react';
import { Check, X } from 'lucide-react';

/**
 * GuardianAI Password Strength Meter Component
 * Purpose: Evaluates password complexity in real-time and displays visual progress bar + requirements checklist.
 */

interface PasswordStrengthMeterProps {
  password: string;
}

export const PasswordStrengthMeter: React.FC<PasswordStrengthMeterProps> = ({ password = '' }) => {
  const hasLength = password.length >= 8;
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[^A-Za-z0-9]/.test(password);

  const passedCount = [hasLength, hasUpper, hasLower, hasNumber, hasSpecial].filter(Boolean).length;

  const getStrengthColor = () => {
    if (passedCount <= 2) return 'bg-red-500';
    if (passedCount <= 4) return 'bg-amber-400';
    return 'bg-emerald-500';
  };

  const getStrengthText = () => {
    if (passedCount <= 2) return 'Weak';
    if (passedCount <= 4) return 'Moderate';
    return 'Strong Security';
  };

  if (!password) return null;

  return (
    <div className="space-y-2 pt-1 text-xs">
      {/* Strength Bar */}
      <div className="flex items-center justify-between font-bold">
        <span className="text-slate-400">Password Strength:</span>
        <span
          className={
            passedCount <= 2
              ? 'text-red-400'
              : passedCount <= 4
              ? 'text-amber-400'
              : 'text-emerald-400'
          }
        >
          {getStrengthText()}
        </span>
      </div>

      <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden flex gap-1">
        {[1, 2, 3, 4, 5].map((level) => (
          <div
            key={level}
            className={`h-full flex-1 transition-all duration-300 ${
              level <= passedCount ? getStrengthColor() : 'bg-slate-800'
            }`}
          />
        ))}
      </div>

      {/* Checklist */}
      <div className="grid grid-cols-2 gap-1.5 pt-1 text-[11px]">
        <div className={`flex items-center gap-1 ${hasLength ? 'text-emerald-400' : 'text-slate-500'}`}>
          {hasLength ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
          <span>8+ characters</span>
        </div>
        <div className={`flex items-center gap-1 ${hasUpper ? 'text-emerald-400' : 'text-slate-500'}`}>
          {hasUpper ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
          <span>Uppercase letter</span>
        </div>
        <div className={`flex items-center gap-1 ${hasNumber ? 'text-emerald-400' : 'text-slate-500'}`}>
          {hasNumber ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
          <span>Number (0-9)</span>
        </div>
        <div className={`flex items-center gap-1 ${hasSpecial ? 'text-emerald-400' : 'text-slate-500'}`}>
          {hasSpecial ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
          <span>Special symbol</span>
        </div>
      </div>
    </div>
  );
};
