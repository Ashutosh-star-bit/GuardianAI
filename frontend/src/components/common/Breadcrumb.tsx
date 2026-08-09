import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';

/**
 * GuardianAI Accessible Breadcrumb Navigation Component
 */

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

export interface BreadcrumbProps {
  items: BreadcrumbItem[];
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({ items }) => {
  return (
    <nav aria-label="Breadcrumb" className="flex items-center text-xs font-bold text-slate-400">
      <ol className="flex items-center gap-1.5 flex-wrap">
        <li>
          <Link to="/" className="flex items-center gap-1 hover:text-white transition-colors">
            <Home className="w-3.5 h-3.5" />
            <span>Home</span>
          </Link>
        </li>

        {items.map((item, idx) => (
          <li key={idx} className="flex items-center gap-1.5">
            <ChevronRight className="w-3.5 h-3.5 text-slate-600 shrink-0" />
            {item.href ? (
              <Link to={item.href} className="hover:text-white transition-colors">
                {item.label}
              </Link>
            ) : (
              <span className="text-sky-400 font-bold">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};
