import React, { useState } from 'react';
import { ShieldCheck, CreditCard, CheckCircle2, Lock, ArrowRight, X, Building2, Smartphone } from 'lucide-react';
import { useAuth, SubscriptionTier } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import { Button } from '../common/Button';

interface PaymentCheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedPlan: {
    tier: SubscriptionTier;
    name: string;
    price: string;
    period: string;
    features: string[];
  };
}

export const PaymentCheckoutModal: React.FC<PaymentCheckoutModalProps> = ({ isOpen, onClose, selectedPlan }) => {
  const { upgradeSubscription, currentUser } = useAuth();
  const { showToast } = useToast();
  const [paymentMethod, setPaymentMethod] = useState<'CARD' | 'UPI' | 'NET_BANKING'>('CARD');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  // Form Fields
  const [cardNumber, setCardNumber] = useState('4242 •••• •••• 4242');
  const [cardExpiry, setCardExpiry] = useState('12/28');
  const [cvv, setCvv] = useState('888');
  const [upiId, setUpiId] = useState('user@okaxis');

  if (!isOpen) return null;

  const handleProcessPayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);

    // Simulate Payment Processing SLA (Stripe / Razorpay API Gateway)
    setTimeout(() => {
      upgradeSubscription(selectedPlan.tier);
      setIsProcessing(false);
      setIsSuccess(true);
      showToast('success', 'Payment Successful!', `Your account has been upgraded to ${selectedPlan.name}. All features unlocked!`);

      setTimeout(() => {
        setIsSuccess(false);
        onClose();
      }, 1800);
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 sm:p-8 space-y-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800/50 hover:bg-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        {isSuccess ? (
          <div className="text-center py-8 space-y-4">
            <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 rounded-full flex items-center justify-center mx-auto animate-bounce">
              <CheckCircle2 className="w-10 h-10" />
            </div>
            <h3 className="text-2xl font-black text-white">Payment Confirmed!</h3>
            <p className="text-sm text-slate-300">
              Your subscription to <strong className="text-sky-400">{selectedPlan.name}</strong> is active. Payout deposited to linked bank account.
            </p>
          </div>
        ) : (
          <>
            {/* Header */}
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-sky-400 text-xs font-bold uppercase tracking-wider">
                <ShieldCheck className="w-4 h-4" />
                <span>256-Bit SSL Encrypted Checkout</span>
              </div>
              <h2 className="text-2xl font-black text-white tracking-tight">Checkout: {selectedPlan.name}</h2>
              <p className="text-xs text-slate-400">
                Amount: <strong className="text-white text-base">{selectedPlan.price}</strong> {selectedPlan.period}
              </p>
            </div>

            {/* Merchant Payout Info Note */}
            <div className="bg-sky-950/40 border border-sky-500/30 rounded-xl p-3 text-xs text-sky-200 space-y-1">
              <div className="font-bold flex items-center gap-1.5 text-sky-300">
                <Building2 className="w-4 h-4 text-sky-400" />
                <span>Direct Bank Account Transfer Active</span>
              </div>
              <p className="text-[11px] opacity-90">
                Payments are processed via Stripe Connect / Razorpay Payouts and deposited directly into your registered bank account.
              </p>
            </div>

            {/* Payment Method Selector */}
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setPaymentMethod('CARD')}
                className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-xs font-bold transition-all ${
                  paymentMethod === 'CARD'
                    ? 'bg-sky-500/20 border-sky-400 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <CreditCard className="w-5 h-5 mb-1 text-sky-400" />
                <span>Card</span>
              </button>
              <button
                type="button"
                onClick={() => setPaymentMethod('UPI')}
                className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-xs font-bold transition-all ${
                  paymentMethod === 'UPI'
                    ? 'bg-sky-500/20 border-sky-400 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Smartphone className="w-5 h-5 mb-1 text-emerald-400" />
                <span>UPI / QR</span>
              </button>
              <button
                type="button"
                onClick={() => setPaymentMethod('NET_BANKING')}
                className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-xs font-bold transition-all ${
                  paymentMethod === 'NET_BANKING'
                    ? 'bg-sky-500/20 border-sky-400 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                <Building2 className="w-5 h-5 mb-1 text-amber-400" />
                <span>Net Banking</span>
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleProcessPayment} className="space-y-4">
              {paymentMethod === 'CARD' && (
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-bold text-slate-300 block mb-1">Card Number</label>
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:border-sky-400 outline-none"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-bold text-slate-300 block mb-1">Expiry Date</label>
                      <input
                        type="text"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:border-sky-400 outline-none"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-bold text-slate-300 block mb-1">CVV Security Code</label>
                      <input
                        type="password"
                        value={cvv}
                        onChange={(e) => setCvv(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:border-sky-400 outline-none"
                      />
                    </div>
                  </div>
                </div>
              )}

              {paymentMethod === 'UPI' && (
                <div>
                  <label className="text-xs font-bold text-slate-300 block mb-1">UPI ID / VPA Handle</label>
                  <input
                    type="text"
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    placeholder="name@upi"
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:border-sky-400 outline-none"
                  />
                </div>
              )}

              {paymentMethod === 'NET_BANKING' && (
                <div>
                  <label className="text-xs font-bold text-slate-300 block mb-1">Select Bank</label>
                  <select className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white focus:border-sky-400 outline-none">
                    <option>HDFC Bank</option>
                    <option>ICICI Bank</option>
                    <option>State Bank of India (SBI)</option>
                    <option>Axis Bank</option>
                  </select>
                </div>
              )}

              <Button
                type="submit"
                disabled={isProcessing}
                className="w-full py-3 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black flex items-center justify-center gap-2 rounded-xl text-sm"
              >
                {isProcessing ? (
                  <span>Processing Payment...</span>
                ) : (
                  <>
                    <Lock className="w-4 h-4" />
                    <span>Pay {selectedPlan.price} & Unlock Plan</span>
                  </>
                )}
              </Button>
            </form>
          </>
        )}
      </div>
    </div>
  );
};
