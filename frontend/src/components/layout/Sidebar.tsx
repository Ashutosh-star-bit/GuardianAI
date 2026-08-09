import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  MessageSquare,
  Mail,
  Globe,
  QrCode,
  History,
  BarChart3,
  FileText,
  User,
  Settings,
  Home,
  X,
  Menu,
  ShieldCheck,
  ShieldAlert,
  ChevronRight,
  LogOut,
  LogIn,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
  onOpenMobileMenu?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen = false, onClose, onOpenMobileMenu }) => {
  const { isAuthenticated, currentUser, logout, effectiveTier } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    if (onClose) onClose();
    navigate('/');
  };

  const mainHubItems = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/community', label: 'Community Intel', icon: ShieldAlert },
  ];

  const scannerItems = [
    { to: '/scan/message', label: 'Message Scan', icon: MessageSquare },
    { to: '/scan/email', label: 'Email Scan', icon: Mail },
    { to: '/scan/url', label: 'URL Scan', icon: Globe },
    { to: '/scan/qr', label: 'QR Scan', icon: QrCode },
  ];

  const intelligenceItems = [
    { to: '/history', label: 'History Log', icon: History },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
    { to: '/reports', label: 'Fraud Reports', icon: FileText },
  ];

  const accountItems = [
    { to: '/profile', label: 'Profile', icon: User },
    { to: '/settings', label: 'System Settings', icon: Settings },
  ];

  const renderNavLink = (item: { to: string; label: string; icon: React.ElementType }) => {
    const Icon = item.icon;
    return (
      <NavLink
        key={item.to}
        to={item.to}
        end={item.to === '/'}
        onClick={onClose}
        className={({ isActive }) =>
          `flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all group ${
            isActive
              ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30 shadow-sm'
              : 'text-slate-300 hover:text-white hover:bg-slate-900/80'
          }`
        }
      >
        <div className="flex items-center gap-2.5">
          <Icon className="w-4 h-4 text-sky-400 group-hover:scale-110 transition-transform" />
          <span>{item.label}</span>
        </div>
        <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity" />
      </NavLink>
    );
  };

  const navContent = (
    <div className="space-y-6">
      {/* User Status Card */}
      {isAuthenticated && currentUser && (
        <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl space-y-1.5">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-xl bg-sky-500/20 text-sky-400 font-black text-xs flex items-center justify-center border border-sky-500/30">
              {currentUser.fullName.charAt(0).toUpperCase()}
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-xs font-bold text-white truncate">{currentUser.fullName}</div>
              <div className="text-[10px] text-amber-400 font-extrabold uppercase">{effectiveTier} PLAN</div>
            </div>
          </div>
        </div>
      )}

      {/* Main Hub Section */}
      <div className="space-y-1">
        <h2 className="px-3 text-[10px] font-black tracking-wider text-slate-400 uppercase">Platform Hub</h2>
        <div className="space-y-1">{mainHubItems.map(renderNavLink)}</div>
      </div>

      {/* Inspection Tools Section */}
      <div className="space-y-1">
        <h2 className="px-3 text-[10px] font-black tracking-wider text-slate-400 uppercase">Inspection Tools</h2>
        <div className="space-y-1">{scannerItems.map(renderNavLink)}</div>
      </div>

      {/* Intelligence & Audit Section */}
      <div className="space-y-1">
        <h2 className="px-3 text-[10px] font-black tracking-wider text-slate-400 uppercase">Intelligence & Audit</h2>
        <div className="space-y-1">{intelligenceItems.map(renderNavLink)}</div>
      </div>

      {/* Account Section */}
      <div className="space-y-1">
        <h2 className="px-3 text-[10px] font-black tracking-wider text-slate-400 uppercase">Account</h2>
        <div className="space-y-1">{accountItems.map(renderNavLink)}</div>
      </div>

      {/* Auth Action Button */}
      <div className="pt-2 border-t border-slate-800">
        {isAuthenticated ? (
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 rounded-xl text-xs font-bold transition-all"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out / Log Out</span>
          </button>
        ) : (
          <NavLink
            to="/login"
            onClick={onClose}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition-all"
          >
            <LogIn className="w-4 h-4" />
            <span>Sign In / Login</span>
          </NavLink>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden lg:block w-64 shrink-0 pr-6 border-r border-slate-800/80 py-6 min-h-[calc(100vh-4rem)]">
        <div className="sticky top-20">{navContent}</div>
      </aside>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 lg:hidden">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={onClose}
              className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="absolute top-0 left-0 bottom-0 w-72 bg-slate-950 border-r border-slate-800 p-6 overflow-y-auto z-10"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-6 h-6 text-sky-400" />
                  <span className="font-black text-white text-lg">GuardianAI Menu</span>
                </div>
                <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white">
                  <X className="w-5 h-5" />
                </button>
              </div>
              {navContent}
            </motion.aside>
          </div>
        )}
      </AnimatePresence>

      {/* Mobile Bottom Quick Navigation Bar */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-30 bg-slate-950/95 border-t border-slate-800 backdrop-blur px-4 py-2 flex items-center justify-around">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 p-1.5 rounded-xl text-[10px] font-bold transition-all ${
              isActive ? 'text-sky-400' : 'text-slate-400'
            }`
          }
        >
          <Home className="w-5 h-5" />
          <span>Home</span>
        </NavLink>

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 p-1.5 rounded-xl text-[10px] font-bold transition-all ${
              isActive ? 'text-sky-400' : 'text-slate-400'
            }`
          }
        >
          <LayoutDashboard className="w-5 h-5" />
          <span>Dashboard</span>
        </NavLink>

        <NavLink
          to="/scan/message"
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 p-1.5 rounded-xl text-[10px] font-bold transition-all ${
              isActive ? 'text-sky-400' : 'text-slate-400'
            }`
          }
        >
          <MessageSquare className="w-5 h-5" />
          <span>Scan</span>
        </NavLink>

        <button
          type="button"
          onClick={onOpenMobileMenu}
          className="flex flex-col items-center gap-1 p-1.5 rounded-xl text-[10px] font-bold text-sky-400 hover:text-white transition-all"
        >
          <Menu className="w-5 h-5" />
          <span>More ⋯</span>
        </button>
      </nav>
    </>
  );
};
