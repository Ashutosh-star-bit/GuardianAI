import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Search, LogIn, UserPlus } from 'lucide-react';
import { SeniorModeToggle } from './SeniorModeToggle';
import { ThemeToggle } from './ThemeToggle';
import { GlobalAdminSearchModal } from './admin/GlobalAdminSearchModal';

// GuardianAI Main Navbar Component
export const Header: React.FC = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  // Global Ctrl + K Keyboard Shortcut Trigger
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsSearchOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      <header className="bg-slate-950 border-b border-slate-800 sticky top-0 z-40 px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          {/* Brand Logo & Name */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="bg-sky-500/10 p-2 rounded-xl border border-sky-500/30 group-hover:border-sky-400 transition-all">
              <ShieldCheck className="w-7 h-7 text-sky-400" />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tight text-white flex items-center gap-2">
                Guardian<span className="text-sky-400">AI</span>
              </h1>
              <p className="text-xs text-slate-400 hidden sm:block">Explainable Anti-Scam Protection</p>
            </div>
          </Link>

          {/* Global Admin Search Bar & Actions */}
          <div className="flex items-center gap-3 sm:gap-4">
            <button
              onClick={() => setIsSearchOpen(true)}
              className="flex items-center gap-2 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 rounded-xl text-xs font-medium transition-all"
            >
              <Search className="w-4 h-4 text-cyan-400" />
              <span className="hidden sm:inline">Search Platform...</span>
              <kbd className="hidden md:inline bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded text-[10px] font-mono border border-slate-700">Ctrl K</kbd>
            </button>

            {/* Light / Dark Theme & Senior Mode Toggles */}
            <ThemeToggle />
            <SeniorModeToggle />

            {/* Authentication Action Links */}
            <div className="flex items-center gap-2 ml-1">
              <Link
                to="/login"
                className="flex items-center gap-1.5 px-3 py-1.5 bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-xl text-xs font-bold transition-all"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Sign In</span>
              </Link>
              <Link
                to="/register"
                className="hidden md:flex items-center gap-1.5 px-3 py-1.5 bg-sky-500 hover:bg-sky-400 text-slate-950 font-black rounded-xl text-xs transition-all shadow-md shadow-sky-500/20"
              >
                <UserPlus className="w-3.5 h-3.5" />
                <span>Register</span>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Global Admin Search Command Palette Modal */}
      <GlobalAdminSearchModal 
        isOpen={isSearchOpen} 
        onClose={() => setIsSearchOpen(false)} 
      />
    </>
  );
};
