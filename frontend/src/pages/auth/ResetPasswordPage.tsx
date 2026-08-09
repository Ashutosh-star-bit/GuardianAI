import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Lock, Eye, EyeOff, CheckCircle2 } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { PasswordStrengthMeter } from '../../components/auth/PasswordStrengthMeter';

const resetPasswordSchema = z
  .object({
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
      .regex(/[0-9]/, 'Must contain at least one number'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;

export const ResetPasswordPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const { showToast } = useToast();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  const passwordValue = watch('password', '');

  const onSubmit = async (data: ResetPasswordFormData) => {
    setIsLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1400));
      setIsSuccess(true);
      showToast('success', 'Password Updated', 'Your password has been successfully reset.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      showToast('error', 'Reset Failed', 'Failed to update password. Link may be expired.');
    } finally {
      setIsLoading(false);
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
          <h1 className="text-3xl font-black text-white tracking-tight">Set New Password</h1>
          <p className="text-sm text-slate-400">Choose a secure password for your GuardianAI account.</p>
        </div>

        <Card className="space-y-6 border-slate-800 shadow-2xl">
          {isSuccess ? (
            <div className="text-center space-y-4 py-4">
              <div className="bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Password Reset Complete!</h3>
              <p className="text-xs text-slate-300">Redirecting you to the sign in page...</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-300">New Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    {...register('password')}
                    className={`w-full pl-10 pr-10 py-2.5 bg-slate-900 border rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none transition-colors ${
                      errors.password ? 'border-red-500 focus:border-red-500' : 'border-slate-800 focus:border-sky-500'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && <p className="text-xs text-red-400 font-medium">{errors.password.message}</p>}
                <PasswordStrengthMeter password={passwordValue} />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-300">Confirm New Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    {...register('confirmPassword')}
                    className={`w-full pl-10 pr-4 py-2.5 bg-slate-900 border rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none transition-colors ${
                      errors.confirmPassword
                        ? 'border-red-500 focus:border-red-500'
                        : 'border-slate-800 focus:border-sky-500'
                    }`}
                  />
                </div>
                {errors.confirmPassword && (
                  <p className="text-xs text-red-400 font-medium">{errors.confirmPassword.message}</p>
                )}
              </div>

              <Button type="submit" isLoading={isLoading} className="w-full shadow-sky-500/20 shadow-lg">
                Update Password
              </Button>
            </form>
          )}
        </Card>
      </div>
    </PageTransition>
  );
};
