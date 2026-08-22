import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';
import { AdminPerspectiveBar } from '../admin/AdminPerspectiveBar';
import { useAuth } from '../../context/AuthContext';

/**
 * GuardianAI Main Shell Layout Component
 */
export const MainLayout: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  const isHomePage = location.pathname === '/';
  // Render sidebar on all protected pages, AND on Home page if logged in!
  const showSidebar = !isHomePage || isAuthenticated;

  // Auto-close mobile sidebar when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-sky-500 selection:text-white transition-colors duration-200">
      {/* Admin Perspective Switcher Banner */}
      <AdminPerspectiveBar />

      {/* Top Application Navbar Header with Hamburger Trigger */}
      <Navbar onOpenMobileMenu={() => setIsMobileMenuOpen(true)} />

      <div className={`flex-1 flex w-full mx-auto ${showSidebar ? 'max-w-7xl 2xl:max-w-[1600px]' : 'max-w-none'}`}>
        {/* Render Sidebar when showSidebar is true */}
        {showSidebar && (
          <Sidebar
            isOpen={isMobileMenuOpen}
            onClose={() => setIsMobileMenuOpen(false)}
            onOpenMobileMenu={() => setIsMobileMenuOpen(true)}
          />
        )}

        {/* Main Content Area Container */}
        <main className={`flex-1 overflow-x-hidden min-w-0 pb-20 lg:pb-6 ${showSidebar ? 'px-3 sm:px-6 py-4 sm:py-6' : 'px-0 py-0'}`}>
          <Outlet />
        </main>
      </div>

      {/* Application Footer */}
      <Footer />
    </div>
  );
};
