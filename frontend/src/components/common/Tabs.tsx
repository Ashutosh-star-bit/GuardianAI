import React from 'react';
import { motion } from 'framer-motion';

/**
 * GuardianAI Accessible Tab Switcher Component
 */

export interface TabItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (id: string) => void;
}

export const Tabs: React.FC<TabsProps> = ({ tabs, activeTab, onChange }) => {
  return (
    <div className="flex items-center gap-1 bg-slate-900 p-1.5 rounded-2xl border border-slate-800 w-fit">
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`relative px-4 py-2 rounded-xl text-xs font-bold transition-colors flex items-center gap-2 ${
              isActive ? 'text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            {isActive && (
              <motion.div
                layoutId="activeTabBackground"
                className="absolute inset-0 bg-sky-600 rounded-xl shadow-md"
                transition={{ type: 'spring', duration: 0.3 }}
              />
            )}
            <span className="relative z-10 flex items-center gap-1.5">
              {tab.icon}
              {tab.label}
            </span>
          </button>
        );
      })}
    </div>
  );
};
