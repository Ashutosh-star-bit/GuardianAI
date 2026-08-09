import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  User as UserIcon,
  Mail,
  Lock,
  LogOut,
  ShieldCheck,
  Zap,
  CreditCard,
  Building2,
  Crown,
  Sparkles,
} from 'lucide-react';

import { PageTransition } from '../components/common/PageTransition';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { useToast } from '../context/ToastContext';
import { useAuth, SubscriptionTier } from '../context/AuthContext';
import { PaymentCheckoutModal } from '../components/payment/PaymentCheckoutModal';
import { ThreeDCard } from '../components/3d/ThreeDCard';

export const ProfilePage: React.FC = () => {
  const { currentUser, logout, effectiveTier, isAdmin } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [checkoutModalOpen, setCheckoutModalOpen] = useState(false);
  const [selectedPlanForCheckout, setSelectedPlanForCheckout] = useState<{
    tier: SubscriptionTier;
    name: string;
    price: string;
    period: string;
    features: string[];
  }>({
    tier: 'PRO',
    name: 'Pro Personal Plan',
    price: '$4.99',
    period: '/month',
    features: ['Unlimited AI Scans', 'Email Header BEC Scanner', 'Quishing QR Scanner', 'Priority Fast Queue'],
  });

  const handleLogout = () => {
    logout();
    showToast('success', 'Logged Out', 'You have been logged out successfully.');
    navigate('/');
  };

  const handleOpenUpgrade = (tier: SubscriptionTier, name: string, price: string, period: string, features: string[]) => {
    setSelectedPlanForCheckout({ tier, name, price, period, features });
    setCheckoutModalOpen(true);
  };

  return (
    <PageTransition className="space-y-8 py-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-sky-400 font-bold text-xs uppercase tracking-wider mb-1">
            <UserIcon className="w-4 h-4" />
            <span>Account Profile & Subscription</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">User Account & Settings</h1>
          <p className="text-xs sm:text-sm text-slate-400">
            View real account credentials, active subscription tier, and security settings.
          </p>
        </div>

        <Button
          onClick={handleLogout}
          variant="secondary"
          className="bg-red-500/10 hover:bg-red-500/20 text-red-400 border-red-500/30 flex items-center gap-2 font-bold text-xs py-2 px-4"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out / Log Out</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Card */}
        <Card className="space-y-6 border-slate-800 bg-slate-900/90">
          <div className="text-center space-y-3 pb-4 border-b border-slate-800">
            <div className="w-20 h-20 rounded-2xl bg-sky-500/10 border-2 border-sky-500/30 flex items-center justify-center mx-auto text-sky-400">
              <UserIcon className="w-10 h-10" />
            </div>
            <div>
              <h2 className="text-xl font-black text-white">{currentUser?.fullName || 'Active User'}</h2>
              <p className="text-xs text-slate-400 flex items-center justify-center gap-1 mt-0.5">
                <Mail className="w-3.5 h-3.5" />
                <span>{currentUser?.email || 'user@guardianai.io'}</span>
              </p>
            </div>

            <div className="inline-flex items-center gap-2 px-3 py-1 bg-sky-500/10 border border-sky-500/30 rounded-full text-xs font-bold text-sky-300">
              {isAdmin ? <Crown className="w-3.5 h-3.5 text-amber-400" /> : <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />}
              <span>{isAdmin ? 'Master Administrator' : 'Standard User Account'}</span>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">User Account ID:</span>
              <span className="font-mono text-white font-bold">{currentUser?.id || 'usr_demo_123'}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Active Subscription:</span>
              <span className="font-extrabold text-amber-400">{effectiveTier} TIER</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Monthly AI Scans Used:</span>
              <span className="font-bold text-white">
                {currentUser?.scanCount || 0} / {effectiveTier === 'FREE' ? '15 Scans' : 'Unlimited'}
              </span>
            </div>
          </div>
        </Card>

        {/* Subscription Tier Management Card */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="space-y-6 border-slate-800 bg-slate-900/90">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
                <Crown className="w-5 h-5" />
                <span>Subscription Plan & Payout Upgrade</span>
              </div>
              <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 rounded-full font-bold">
                Current Plan: {effectiveTier}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Pro Tier Upgrade Card (3D Tilt) */}
              <ThreeDCard glowColor="cyan">
                <div className="bg-slate-950/90 border border-sky-500/40 rounded-2xl p-5 space-y-4 relative backdrop-blur-xl h-full flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-black text-white">Pro Personal</h3>
                        <p className="text-xs text-slate-400">Unlimited threat inspection for individuals.</p>
                      </div>
                      <span className="text-lg font-black text-sky-400 font-mono">$4.99 / ₹399</span>
                    </div>
                    <ul className="text-xs text-slate-300 space-y-1.5 font-medium">
                      <li className="flex items-center gap-1.5">✓ Unlimited AI Scans</li>
                      <li className="flex items-center gap-1.5">✓ Email Header BEC Scanner</li>
                      <li className="flex items-center gap-1.5">✓ Quishing QR Scanner</li>
                      <li className="flex items-center gap-1.5">✓ Priority Fast-Queue AI</li>
                    </ul>
                  </div>
                  <Button
                    onClick={() =>
                      handleOpenUpgrade('PRO', 'Pro Personal Plan', '$4.99 / ₹399', '/month', [
                        'Unlimited AI Scans',
                        'Email Header BEC Scanner',
                        'Quishing QR Scanner',
                        'Priority Fast-Queue AI',
                      ])
                    }
                    className="w-full py-2 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black text-xs rounded-xl shadow-lg shadow-sky-500/20"
                  >
                    Upgrade to Pro ($4.99 / ₹399/mo)
                  </Button>
                </div>
              </ThreeDCard>

              {/* Business SMB Card (3D Tilt) */}
              <ThreeDCard glowColor="purple">
                <div className="bg-slate-950/90 border border-purple-500/40 rounded-2xl p-5 space-y-4 relative backdrop-blur-xl h-full flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="text-lg font-black text-white">Business SMB</h3>
                        <p className="text-xs text-slate-400">Team security dashboard & developer API.</p>
                      </div>
                      <span className="text-lg font-black text-purple-400 font-mono">$14.99 / ₹1,199</span>
                    </div>
                    <ul className="text-xs text-slate-300 space-y-1.5 font-medium">
                      <li className="flex items-center gap-1.5">✓ Everything in Pro</li>
                      <li className="flex items-center gap-1.5">✓ Team Threat Dashboard</li>
                      <li className="flex items-center gap-1.5">✓ Developer API Keys</li>
                      <li className="flex items-center gap-1.5">✓ 1-Click Fraud Reporting</li>
                    </ul>
                  </div>
                  <Button
                    onClick={() =>
                      handleOpenUpgrade('BUSINESS', 'Business SMB Plan', '$14.99 / ₹1,199', '/month per seat', [
                        'Everything in Pro',
                        'Team Threat Dashboard',
                        'Developer API Access',
                        '1-Click FTC Fraud Reporting',
                      ])
                    }
                    className="w-full py-2 bg-purple-500 hover:bg-purple-400 text-white font-black text-xs rounded-xl shadow-lg shadow-purple-500/20"
                  >
                    Upgrade to Business ($14.99 / ₹1,199/mo)
                  </Button>
                </div>
              </ThreeDCard>
            </div>
          </Card>
        </div>
      </div>

      <PaymentCheckoutModal
        isOpen={checkoutModalOpen}
        onClose={() => setCheckoutModalOpen(false)}
        selectedPlan={selectedPlanForCheckout}
      />
    </PageTransition>
  );
};
