import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Lock, Menu } from 'lucide-react';
import { SeniorModeToggle } from '../SeniorModeToggle';
import { ThemeToggle } from '../ThemeToggle';

/**
 * GuardianAI Navbar Layout Component
 * Purpose: Top header rendering brand logo, Edge PII status, Theme Switcher, Senior Mode Toggle, and Mobile Hamburger Trigger.
 */

export interface NavbarProps {
  onOpenMobileMenu?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenMobileMenu }) => {
  return (
    <header className="bg-slate-950/95 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40 px-3 py-2 sm:px-4 sm:py-2.5">
      <div className="max-w-7xl 2xl:max-w-[1600px] mx-auto flex items-center justify-between gap-2">
        {/* Brand Logo & Hamburger Menu Button */}
        <div className="flex items-center gap-2">
          {/* Hamburger Menu Trigger for Mobile & Half-Screen Laptops */}
          <button
            type="button"
            onClick={onOpenMobileMenu}
            className="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-900 border border-slate-800 transition-colors"
            title="Open Platform Navigation Menu"
            aria-label="Open Platform Navigation Menu"
          >
            <Menu className="w-5 h-5 text-sky-400" />
          </button>

          <Link to="/" className="flex items-center gap-2 sm:gap-3 hover:opacity-90 transition-opacity shrink-0">
            <div className="bg-sky-500/10 p-1.5 sm:p-2 rounded-xl border border-sky-500/30 shrink-0">
              <ShieldCheck className="w-5 h-5 sm:w-6 sm:h-6 text-sky-400" />
            </div>
            <div>
              <h1 className="text-base sm:text-xl font-black tracking-tight text-white flex items-center gap-1">
                Guardian<span className="text-sky-400">AI</span>
              </h1>
            </div>
          </Link>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
          <div className="hidden xl:flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            <span>Edge PII Scrubbing Active</span>
          </div>

          {/* Dedicated Theme Toggle Switch (Dark / Light) */}
          <ThemeToggle />

          {/* Dedicated Senior Mode Trigger Button */}
          <SeniorModeToggle />
        </div>
      </div>
    </header>
  );
};

export const Header = Navbar;
