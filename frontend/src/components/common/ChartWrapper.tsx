import React from 'react';
import { Card } from './Card';

/**
 * GuardianAI Responsive Chart Wrapper Component
 */

export interface ChartWrapperProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export const ChartWrapper: React.FC<ChartWrapperProps> = ({
  title,
  subtitle,
  action,
  children,
  className = '',
}) => {
  return (
    <Card className={`space-y-4 border-slate-800 ${className}`}>
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-black text-white">{title}</h3>
          {subtitle && <p className="text-xs text-slate-400">{subtitle}</p>}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div className="w-full overflow-hidden">{children}</div>
    </Card>
  );
};
