import React, { useEffect } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { useAccessibility } from '../context/AccessibilityContext';

/**
 * GuardianAI Senior Citizen Mode Toggle Component
 * Purpose: Dedicated button trigger for Senior Citizen High-Contrast Accessibility Mode with mobile-optimized responsive layout.
 */
export const SeniorModeToggle: React.FC = () => {
  const { isSeniorMode, toggleSeniorMode } = useAccessibility();

  // Keyboard shortcut listener (Alt + S)
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.altKey && (event.key === 's' || event.key === 'S')) {
        event.preventDefault();
        toggleSeniorMode();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleSeniorMode]);

  return (
    <button
      onClick={toggleSeniorMode}
      className={`flex items-center gap-1.5 sm:gap-2 px-2.5 sm:px-3.5 py-1.5 rounded-xl font-extrabold transition-all border-2 shadow-sm shrink-0 whitespace-nowrap ${
        isSeniorMode
          ? 'bg-amber-400 text-black border-black hover:bg-amber-300'
          : 'bg-slate-900 text-amber-300 border-amber-400/70 hover:bg-slate-800'
      }`}
      aria-label="Toggle Senior Citizen High-Contrast Mode (Hotkey: Alt + S)"
      title="Toggle Senior Mode (Hotkey: Alt + S)"
    >
      {isSeniorMode ? (
        <EyeOff className="w-4 h-4 text-black shrink-0" />
      ) : (
        <Eye className="w-4 h-4 text-amber-400 shrink-0" />
      )}
      
      <span className="text-xs sm:text-sm font-black">
        <span className="hidden sm:inline">Senior Mode: </span>
        <span className="sm:hidden">Senior: </span>
        <span>{isSeniorMode ? 'ON' : 'OFF'}</span>
      </span>

      <span className="text-[10px] opacity-75 font-mono px-1 py-0.5 rounded border border-current hidden lg:inline-block">
        Alt+S
      </span>
    </button>
  );
};
