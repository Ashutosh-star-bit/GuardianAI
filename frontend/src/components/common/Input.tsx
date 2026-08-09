import React, { forwardRef } from 'react';

/**
 * GuardianAI Accessible Reusable Input Component
 * Purpose: Provides a styled input field with label, error states, and left/right icon slots.
 */

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, leftIcon, rightIcon, className = '', id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

    return (
      <div className="space-y-1.5 w-full">
        {label && (
          <label htmlFor={inputId} className="block text-xs font-bold text-slate-300">
            {label}
          </label>
        )}

        <div className="relative flex items-center">
          {leftIcon && <div className="absolute left-3.5 text-slate-400 pointer-events-none">{leftIcon}</div>}

          <input
            id={inputId}
            ref={ref}
            className={`w-full py-2.5 bg-slate-900 border rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none transition-colors ${
              leftIcon ? 'pl-10' : 'pl-3.5'
            } ${rightIcon ? 'pr-10' : 'pr-3.5'} ${
              error ? 'border-red-500 focus:border-red-500' : 'border-slate-800 focus:border-sky-500'
            } ${className}`}
            {...props}
          />

          {rightIcon && <div className="absolute right-3.5 text-slate-400">{rightIcon}</div>}
        </div>

        {error && <p className="text-xs text-red-400 font-medium">{error}</p>}
        {helperText && !error && <p className="text-[11px] text-slate-500">{helperText}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';
