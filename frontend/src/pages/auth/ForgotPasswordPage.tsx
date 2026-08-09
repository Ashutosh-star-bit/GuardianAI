import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Mail, ArrowLeft, Send, CheckCircle2 } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';

const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
});

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

export const ForgotPasswordPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 1200));
      setIsSubmitted(true);
      showToast('success', 'Reset Link Sent', 'Check your email inbox for reset instructions.');
    } catch (err) {
      showToast('error', 'Request Failed', 'Failed to send reset link.');
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
          <h1 className="text-3xl font-black text-white tracking-tight">Forgot Password?</h1>
          <p className="text-sm text-slate-400">Enter your account email to receive a password reset link.</p>
        </div>

        <Card className="space-y-6 border-slate-800 shadow-2xl">
          {isSubmitted ? (
            <div className="text-center space-y-4 py-4">
              <div className="bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-full w-12 h-12 flex items-center justify-center mx-auto text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Reset Link Dispatched</h3>
              <p className="text-xs text-slate-300 leading-relaxed">
                If an account exists with that email address, you will receive password reset instructions shortly.
              </p>
              <Link to="/login" className="inline-block">
                <Button variant="secondary" size="sm">
                  Return to Login
                </Button>
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-300">Registered Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    placeholder="name@company.com"
                    {...register('email')}
                    className={`w-full pl-10 pr-4 py-2.5 bg-slate-900 border rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none transition-colors ${
                      errors.email ? 'border-red-500 focus:border-red-500' : 'border-slate-800 focus:border-sky-500'
                    }`}
                  />
                </div>
                {errors.email && <p className="text-xs text-red-400 font-medium">{errors.email.message}</p>}
              </div>

              <Button
                type="submit"
                isLoading={isLoading}
                className="w-full shadow-sky-500/20 shadow-lg"
                rightIcon={<Send className="w-4 h-4" />}
              >
                Send Reset Password Link
              </Button>
            </form>
          )}

          <div className="text-center pt-2 border-t border-slate-900">
            <Link to="/login" className="text-xs text-slate-400 hover:text-white flex items-center justify-center gap-1">
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Sign In</span>
            </Link>
          </div>
        </Card>
      </div>
    </PageTransition>
  );
};
