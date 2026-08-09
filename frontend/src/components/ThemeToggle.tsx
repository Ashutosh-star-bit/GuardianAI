import React, { useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';
import { useAccessibility } from '../context/AccessibilityContext';

/**
 * GuardianAI Theme Toggle Switch Component
 * Purpose: Independent Light/Dark theme toggle button trigger with Alt + T hotkey support.
 */
export const ThemeToggle: React.FC = () => {
  const { isDarkMode, toggleTheme } = useAccessibility();

  // Keyboard shortcut listener (Alt + T)
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.altKey && (event.key === 't' || event.key === 'T')) {
        event.preventDefault();
        toggleTheme();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleTheme]);

  return (
    <button
      onClick={toggleTheme}
      className={`flex items-center gap-1.5 sm:gap-2.5 px-2 sm:px-3 py-1.5 rounded-xl font-bold transition-all border shadow-sm shrink-0 whitespace-nowrap ${
        isDarkMode
          ? 'bg-slate-900 text-slate-200 border-slate-700 hover:bg-slate-800'
          : 'bg-amber-100 text-amber-950 border-amber-300 hover:bg-amber-200'
      }`}
      aria-label="Toggle Light/Dark Theme (Hotkey: Alt + T)"
      title="Toggle Light/Dark Theme (Hotkey: Alt + T)"
    >
      {/* Sliding Key Switch Graphic */}
      <div
        className={`w-7 sm:w-8 h-4 sm:h-4.5 rounded-full p-0.5 flex items-center transition-colors shrink-0 ${
          isDarkMode ? 'bg-sky-600' : 'bg-amber-400'
        }`}
      >
        <div
          className={`w-3 sm:w-3.5 h-3 sm:h-3.5 rounded-full bg-white shadow-md transform transition-transform ${
            isDarkMode ? 'translate-x-3 sm:translate-x-3.5' : 'translate-x-0'
          }`}
        />
      </div>

      <div className="flex items-center gap-1 text-xs font-semibold">
        {isDarkMode ? <Moon className="w-3.5 h-3.5 text-sky-400" /> : <Sun className="w-3.5 h-3.5 text-amber-600" />}
        <span className="hidden xs:inline sm:inline">{isDarkMode ? 'Dark' : 'Light'}</span>
        <span className="text-[10px] opacity-60 font-mono hidden lg:inline-block">Alt+T</span>
      </div>
    </button>
  );
};
