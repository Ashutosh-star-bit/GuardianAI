import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ShieldCheck, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { PageTransition } from '../../components/common/PageTransition';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { useToast } from '../../context/ToastContext';
import { useAuth } from '../../context/AuthContext';

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { showToast } = useToast();
  const { login, socialLogin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const fromPath = (location.state as any)?.from?.pathname || '/';

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    try {
      const res = await login(data.email, data.password);
      setIsLoading(false);

      if (res.success) {
        showToast('success', 'Authentication Successful', res.message);
        navigate(fromPath, { replace: true });
      } else {
        showToast('error', 'Login Failed', res.message);
      }
    } catch (err) {
      setIsLoading(false);
      showToast('error', 'Login Failed', 'Invalid email or password.');
    }
  };

  const handleSocialClick = async (provider: 'google' | 'github' | 'facebook') => {
    setIsLoading(true);
    try {
      const res = await socialLogin(provider);
      setIsLoading(false);
      showToast('success', `${provider.toUpperCase()} Sign-In Successful`, res.message);
      navigate(fromPath, { replace: true });
    } catch (err) {
      setIsLoading(false);
      showToast('error', 'Social Login Failed', `Could not authenticate via ${provider}.`);
    }
  };

  return (
    <PageTransition className="min-h-[85vh] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <Link to="/" className="inline-flex items-center gap-2 group">
            <div className="bg-sky-500/10 p-2.5 rounded-2xl border border-sky-500/30 group-hover:border-sky-400 transition-all">
              <ShieldCheck className="w-8 h-8 text-sky-400" />
            </div>
          </Link>
          <h1 className="text-3xl font-black text-white tracking-tight">Welcome Back</h1>
          <p className="text-sm text-slate-400">Sign in to your GuardianAI threat protection console.</p>
        </div>

        {/* Form Card */}
        <Card className="space-y-6 border-slate-800 bg-slate-900/90">
          {/* Social OAuth SSO Login Buttons */}
          <div className="grid grid-cols-2 gap-2.5">
            <button
              type="button"
              onClick={() => handleSocialClick('google')}
              className="flex items-center justify-center gap-2 py-2.5 px-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-xs font-bold text-white transition-all group cursor-pointer"
            >
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24">
                <path
                  fill="#EA4335"
                  d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.3 9 5 12 5z"
                />
                <path
                  fill="#4285F4"
                  d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.3s.2-1.6.4-2.3L1.9 7.3C.7 9.7 0 10.8 0 12.5s.7 2.8 1.9 5.2l3.7-2.9z"
                />
                <path
                  fill="#34A853"
                  d="M12 24c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.3-6.4-5.2L1.9 17C3.7 20.7 7.5 24 12 24z"
                />
              </svg>
              <span>Google</span>
            </button>

            <button
              type="button"
              onClick={() => handleSocialClick('github')}
              className="flex items-center justify-center gap-2 py-2.5 px-3 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-xs font-bold text-white transition-all cursor-pointer"
            >
              <svg className="w-4 h-4 fill-current text-white" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
              <span>GitHub</span>
            </button>
          </div>

          <div className="flex items-center gap-3 my-4">
            <div className="h-[1px] bg-slate-800 flex-1" />
            <span className="text-[10px] text-slate-500 font-bold uppercase">or email sign in</span>
            <div className="h-[1px] bg-slate-800 flex-1" />
          </div>

          {/* Email / Password Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="text-xs font-bold text-slate-300 block mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="email"
                  {...register('email')}
                  placeholder="user@example.com"
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
                  className="absolute right-3 top-3 text-slate-400 hover:text-white"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
              {errors.password && <p className="text-xs text-red-400 mt-1">{errors.password.message}</p>}
            </div>

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black rounded-xl text-sm"
            >
              {isLoading ? 'Authenticating...' : 'Sign In to Console'}
            </Button>
          </form>

          <div className="text-center pt-2 border-t border-slate-800 text-xs text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-sky-400 font-bold hover:underline">
              Create Account
            </Link>
          </div>
        </Card>
      </div>
    </PageTransition>
  );
};
