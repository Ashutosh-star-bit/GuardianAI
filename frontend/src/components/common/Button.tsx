import React from 'react';
import { Loader2 } from 'lucide-react';

/**
 * GuardianAI Reusable Button Component
 * Purpose: Provides a standardized, accessible button supporting primary, secondary, danger, and loading variants.
 */

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-bold rounded-xl transition-all border shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  const variantStyles = {
    primary: 'bg-sky-600 hover:bg-sky-500 text-white border-sky-500 focus:ring-sky-500 shadow-sky-600/20',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700 focus:ring-slate-600',
    danger: 'bg-red-600 hover:bg-red-500 text-white border-red-500 focus:ring-red-500 shadow-red-600/20',
    ghost: 'bg-transparent hover:bg-slate-800 text-slate-300 border-transparent focus:ring-slate-700',
  };

  const sizeStyles = {
    sm: 'text-xs px-3 py-1.5 gap-1.5',
    md: 'text-sm px-4 py-2.5 gap-2',
    lg: 'text-base px-6 py-3.5 gap-2.5',
  };

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : leftIcon}
      <span>{children}</span>
      {!isLoading && rightIcon}
    </button>
  );
};
