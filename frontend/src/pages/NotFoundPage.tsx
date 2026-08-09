import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldAlert, ArrowLeft } from 'lucide-react';
import { Button } from '../components/common/Button';

/**
 * GuardianAI 404 Not Found Page Component
 * Purpose: Friendly, accessible fallback screen when navigating to non-existent application routes.
 */

export const NotFoundPage: React.FC = () => {
  return (
    <div className="py-16 text-center space-y-6 max-w-md mx-auto">
      <div className="bg-slate-900 border border-slate-800 p-4 rounded-full w-20 h-20 mx-auto flex items-center justify-center">
        <ShieldAlert className="w-10 h-10 text-sky-400" />
      </div>

      <div className="space-y-2">
        <h1 className="text-4xl font-black text-white">404</h1>
        <h2 className="text-xl font-bold text-slate-200">Page Not Found</h2>
        <p className="text-sm text-slate-400">
          The page you are looking for doesn't exist or has been moved. Don't worry, your personal safety data remains secure.
        </p>
      </div>

      <Link to="/" className="inline-block">
        <Button leftIcon={<ArrowLeft className="w-4 h-4" />}>
          Return to Home Safety Console
        </Button>
      </Link>
    </div>
  );
};
