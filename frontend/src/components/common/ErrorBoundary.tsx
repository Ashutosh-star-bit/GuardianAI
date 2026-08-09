import React, { Component, ErrorInfo, ReactNode } from 'react';
import { ShieldAlert, RefreshCw } from 'lucide-react';

/**
 * GuardianAI React Error Boundary
 * Purpose: Catches unhandled JavaScript render errors gracefully, preventing full application crashes and offering a 1-click recovery button.
 */

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('GuardianAI ErrorBoundary caught an unhandled error:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: undefined });
    window.location.href = '/';
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 max-w-md w-full text-center space-y-6 shadow-2xl">
            <div className="bg-red-500/10 p-4 rounded-full w-16 h-16 mx-auto flex items-center justify-center border border-red-500/20">
              <ShieldAlert className="w-8 h-8 text-red-500" />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-bold text-white">Something went wrong</h2>
              <p className="text-sm text-slate-400">
                An unexpected UI rendering error occurred. Don't worry, your data and privacy remain secure.
              </p>
            </div>
            <button
              onClick={this.handleReset}
              className="w-full inline-flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-bold px-4 py-2.5 rounded-xl transition-all shadow-lg shadow-sky-600/20"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Return to Safety Dashboard</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
