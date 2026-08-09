import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

/**
 * GuardianAI Accessibility & Theme Context
 * Purpose: Manages independent state for Light/Dark Theme toggle and Senior Citizen Mode, updating body CSS classes dynamically.
 */

interface AccessibilityContextType {
  isDarkMode: boolean;
  isSeniorMode: boolean;
  isAudioNarrationEnabled: boolean;
  toggleTheme: () => void;
  toggleSeniorMode: () => void;
  toggleAudioNarration: () => void;
}

const AccessibilityContext = createContext<AccessibilityContextType | undefined>(undefined);

export const AccessibilityProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(() => {
    return localStorage.getItem('guardianai_theme') !== 'light';
  });

  const [isSeniorMode, setIsSeniorMode] = useState<boolean>(() => {
    return localStorage.getItem('guardianai_senior_mode') === 'true';
  });

  const [isAudioNarrationEnabled, setIsAudioNarrationEnabled] = useState<boolean>(() => {
    return localStorage.getItem('guardianai_audio_narration') === 'true';
  });

  // Independent Theme Toggle Handler
  const toggleTheme = useCallback(() => {
    setIsDarkMode((prev) => {
      const next = !prev;
      localStorage.setItem('guardianai_theme', next ? 'dark' : 'light');
      return next;
    });
  }, []);

  // Independent Senior Mode Toggle Handler
  const toggleSeniorMode = useCallback(() => {
    setIsSeniorMode((prev) => {
      const next = !prev;
      localStorage.setItem('guardianai_senior_mode', String(next));
      return next;
    });
  }, []);

  const toggleAudioNarration = useCallback(() => {
    setIsAudioNarrationEnabled((prev) => !prev);
  }, []);

  // Sync Senior Mode CSS class
  useEffect(() => {
    if (isSeniorMode) {
      document.body.classList.add('senior-mode');
    } else {
      document.body.classList.remove('senior-mode');
    }
  }, [isSeniorMode]);

  // Sync Light/Dark Theme CSS classes dynamically
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark-theme');
      document.body.classList.remove('light-theme');
    } else {
      document.body.classList.add('light-theme');
      document.body.classList.remove('dark-theme');
    }
  }, [isDarkMode]);

  return (
    <AccessibilityContext.Provider
      value={{
        isDarkMode,
        isSeniorMode,
        isAudioNarrationEnabled,
        toggleTheme,
        toggleSeniorMode,
        toggleAudioNarration,
      }}
    >
      {children}
    </AccessibilityContext.Provider>
  );
};

export const useAccessibility = (): AccessibilityContextType => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};
