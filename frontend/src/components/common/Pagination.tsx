import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './Button';

/**
 * GuardianAI Reusable Pagination Component
 */

export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between border-t border-slate-800 pt-4 w-full">
      <Button
        variant="secondary"
        size="sm"
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
        leftIcon={<ChevronLeft className="w-4 h-4" />}
      >
        Previous
      </Button>

      <div className="flex items-center gap-1 text-xs font-bold text-slate-400">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`w-8 h-8 rounded-lg transition-colors ${
              currentPage === page ? 'bg-sky-600 text-white font-black' : 'hover:bg-slate-900 text-slate-400'
            }`}
          >
            {page}
          </button>
        ))}
      </div>

      <Button
        variant="secondary"
        size="sm"
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
        rightIcon={<ChevronRight className="w-4 h-4" />}
      >
        Next
      </Button>
    </div>
  );
};
