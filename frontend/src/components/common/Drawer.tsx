import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

/**
 * GuardianAI Slide-Over Drawer Component
 * Purpose: Renders a side drawer panel for secondary controls and threat details.
 */

export interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  position?: 'left' | 'right';
}

export const Drawer: React.FC<DrawerProps> = ({
  isOpen,
  onClose,
  title,
  children,
  position = 'right',
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const variants = {
    closed: { x: position === 'right' ? '100%' : '-100%' },
    open: { x: 0 },
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-slate-950/70 backdrop-blur-sm"
          />

          <motion.div
            variants={variants}
            initial="closed"
            animate="open"
            exit="closed"
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className={`fixed inset-y-0 ${
              position === 'right' ? 'right-0' : 'left-0'
            } w-full max-w-md bg-slate-900 border-l border-slate-800 p-6 space-y-6 shadow-2xl z-10 flex flex-col justify-between`}
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <h3 className="text-lg font-black text-white">{title}</h3>
                <button
                  onClick={onClose}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="space-y-4">{children}</div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
