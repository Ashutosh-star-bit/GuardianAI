import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';
import { PasswordStrengthMeter } from '../../components/auth/PasswordStrengthMeter';

const registerSchema = z
  .object({
    fullName: z.string().min(2, 'Full name must be at least 2 characters'),
    email: z.string().email('Please enter a valid Gmail / Email address'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

export const RegisterPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { showToast } = useToast();
  const { registerUser, googleSignIn } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const passwordValue = watch('password', '');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      await registerUser(data.email, data.password, data.fullName);
      setIsLoading(false);
      showToast(
        'success',
        'Verification Email Sent!',
        `A verification link has been sent to ${data.email}. Please check your Gmail inbox and click the link.`
      );
      navigate('/verify-email');
    } catch (err: any) {
      setIsLoading(false);
      const code = err?.code;
      if (code === 'auth/email-already-in-use') {
        showToast('error', 'Account Exists', 'An account with this email already exists. Please sign in instead.');
      } else if (code === 'auth/weak-password') {
        showToast('error', 'Weak Password', 'Password must be at least 6 characters long.');
      } else if (code === 'auth/invalid-email') {
        showToast('error', 'Invalid Email', 'Please enter a valid email address.');
      } else {
        showToast('error', 'Registration Failed', err?.message || 'Could not create account. Please try again.');
      }
    }
  };

  const handleGoogleSignUp = async () => {
    setIsLoading(true);
    try {
      const res = await googleSignIn();
      setIsLoading(false);
      if (res.success) {
        showToast('success', 'Google Sign-Up Successful', res.message);
        navigate('/');
      } else {
        showToast('error', 'Google Sign-Up Failed', res.message);
      }
    } catch (err) {
      setIsLoading(false);
      showToast('error', 'Google Sign-Up Failed', 'Could not authenticate via Google. Please try again.');
    }
  };

  return (
    <PageTransition className="min-h-[85vh] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2 group">
            <div className="bg-sky-500/10 p-2.5 rounded-2xl border border-sky-500/30 group-hover:border-sky-400 transition-all">
              <ShieldCheck className="w-8 h-8 text-sky-400" />
            </div>
          </Link>
          <h1 className="text-3xl font-black text-white tracking-tight">Create Account</h1>
          <p className="text-sm text-slate-400">Register with real email verification powered by Google Firebase.</p>
        </div>

        <Card className="space-y-6 border-slate-800 bg-slate-900/90">
          {/* Google SSO — Real Firebase OAuth Popup */}
          <button
            type="button"
            onClick={handleGoogleSignUp}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-slate-950 hover:bg-slate-800 border border-slate-700 rounded-xl text-sm font-bold text-white transition-all cursor-pointer disabled:opacity-50"
          >
            <svg className="w-5 h-5 shrink-0" viewBox="0 0 24 24">
              <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z" />
              <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z" />
              <path fill="#FBBC05" d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 10.8 0 12.5s.7 2.8 1.9 5.2l3.7-2.9z" />
              <path fill="#34A853" d="M12 24c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 17C3.7 20.7 7.5 24 12 24z" />
            </svg>
            <span>Continue with Google</span>
          </button>

          <div className="flex items-center gap-3 my-2">
            <div className="h-[1px] bg-slate-800 flex-1" />
            <span className="text-[10px] text-slate-500 font-bold uppercase">or register with email</span>
            <div className="h-[1px] bg-slate-800 flex-1" />
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="text-xs font-bold text-slate-300 block mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  {...register('fullName')}
                  placeholder="Jane Doe"
                  className="w-full bg-slate-950 border border-slate-800 focus:border-sky-400 text-white text-sm rounded-xl pl-9 pr-3 py-2.5 outline-none transition-all"
                />
              </div>
              {errors.fullName && <p className="text-xs text-red-400 mt-1">{errors.fullName.message}</p>}
            </div>

            <div>
              <label className="text-xs font-bold text-slate-300 block mb-1">Gmail / Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="email"
                  {...register('email')}
                  placeholder="you@gmail.com"
                  className="w-full bg-slate-950 border border-slate-800 focus:border-sky-400 text-white text-sm rounded-xl pl-9 pr-3 py-2.5 outline-none transition-all"
                />
              </div>
              {errors.email && <p className="text-xs text-red-400 mt-1">{errors.email.message}</p>}
            </div>

            <div>
              <label className="text-xs font-bold text-slate-300 block mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  {...register('password')}
                  placeholder="••••••••"
                  className="w-full bg-slate-950 border border-slate-800 focus:border-sky-400 text-white text-sm rounded-xl pl-9 pr-10 py-2.5 outline-none transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-slate-400 hover:text-slate-200"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && <p className="text-xs text-red-400 mt-1">{errors.password.message}</p>}
              <PasswordStrengthMeter password={passwordValue} />
            </div>

            <div>
              <label className="text-xs font-bold text-slate-300 block mb-1">Confirm Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  {...register('confirmPassword')}
                  placeholder="••••••••"
                  className="w-full bg-slate-950 border border-slate-800 focus:border-sky-400 text-white text-sm rounded-xl pl-9 pr-3 py-2.5 outline-none transition-all"
                />
              </div>
              {errors.confirmPassword && (
                <p className="text-xs text-red-400 mt-1">{errors.confirmPassword.message}</p>
              )}
            </div>

            <Button type="submit" isLoading={isLoading} className="w-full py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black rounded-xl text-sm mt-2">
              Create Account & Verify Email
            </Button>
          </form>

          <p className="text-xs text-slate-400 text-center">
            Already have an account?{' '}
            <Link to="/login" className="text-sky-400 hover:underline font-bold">
              Sign in
            </Link>
          </p>
        </Card>
      </div>
    </PageTransition>
  );
};
