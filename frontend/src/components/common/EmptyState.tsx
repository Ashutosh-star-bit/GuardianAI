import React from 'react';
import { Search } from 'lucide-react';
import { Button } from './Button';

/**
 * GuardianAI Reusable Empty State Component
 */

export interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon = <Search className="w-6 h-6 text-slate-500" />,
  title,
  description,
  actionLabel,
  onAction,
}) => {
  return (
    <div className="text-center py-12 px-4 space-y-3">
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-full w-14 h-14 flex items-center justify-center mx-auto">
        {icon}
      </div>
      <h3 className="text-base font-bold text-white">{title}</h3>
      <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">{description}</p>
      {actionLabel && onAction && (
        <div className="pt-2">
          <Button variant="secondary" size="sm" onClick={onAction}>
            {actionLabel}
          </Button>
        </div>
      )}
    </div>
  );
};
