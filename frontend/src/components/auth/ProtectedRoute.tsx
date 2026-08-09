import React from 'react';
import { Navigate, useLocation, Link } from 'react-router-dom';
import { ShieldAlert, LogIn, UserPlus, Lock } from 'lucide-react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const location = useLocation();
  const token = localStorage.getItem('guardianai_access_token');
  const isAuthenticated = Boolean(token);

  if (!isAuthenticated) {
    return (
      <div className="min-h-[75vh] flex items-center justify-center p-4">
        <Card className="max-w-md w-full text-center space-y-6 p-6 sm:p-8 border-amber-500/30 bg-slate-900/90 shadow-2xl">
          <div className="mx-auto w-14 h-14 bg-amber-500/10 border border-amber-500/30 rounded-2xl flex items-center justify-center">
            <Lock className="w-7 h-7 text-amber-400" />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-black tracking-tight text-white">Authentication Required</h2>
            <p className="text-xs sm:text-sm text-slate-300">
              Please sign in to access your security dashboard, scan history logs, threat telemetry, and administrative settings.
            </p>
          </div>

          <div className="pt-2 flex flex-col sm:flex-row gap-3 justify-center">
            <Link to="/login" state={{ from: location }} className="w-full sm:w-auto">
              <Button variant="primary" className="w-full flex items-center justify-center gap-2 py-2.5">
                <LogIn className="w-4 h-4" />
                <span>Sign In to Continue</span>
              </Button>
            </Link>
            <Link to="/register" className="w-full sm:w-auto">
              <Button variant="secondary" className="w-full flex items-center justify-center gap-2 py-2.5">
                <UserPlus className="w-4 h-4" />
                <span>Register Account</span>
              </Button>
            </Link>
          </div>
        </Card>
      </div>
    );
  }

  return <>{children}</>;
};
