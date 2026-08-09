import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './services/api/queryClient';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { AccessibilityProvider } from './context/AccessibilityContext';
import { ToastProvider } from './context/ToastContext';
import { AuthProvider } from './context/AuthContext';
import { MainLayout } from './components/layout/MainLayout';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { CinematicMatrix3DCanvas } from './components/3d/CinematicMatrix3DCanvas';

// Lazy Loaded Pages Strategy for Bundle Code-Splitting
const HomePage = lazy(() => import('./pages/HomePage').then((m) => ({ default: m.HomePage })));
const DashboardPage = lazy(() => import('./pages/DashboardPage').then((m) => ({ default: m.DashboardPage })));
const MessageScanPage = lazy(() => import('./pages/MessageScanPage').then((m) => ({ default: m.MessageScanPage })));
const EmailScanPage = lazy(() => import('./pages/EmailScanPage').then((m) => ({ default: m.EmailScanPage })));
const UrlScanPage = lazy(() => import('./pages/UrlScanPage').then((m) => ({ default: m.UrlScanPage })));
const QrScanPage = lazy(() => import('./pages/QrScanPage').then((m) => ({ default: m.QrScanPage })));
const ScanResultPage = lazy(() => import('./pages/ScanResultPage').then((m) => ({ default: m.ScanResultPage })));
const CommunityDashboardPage = lazy(() => import('./pages/CommunityDashboardPage').then((m) => ({ default: m.CommunityDashboardPage })));
const AdminModerationPanelPage = lazy(() => import('./pages/AdminModerationPanelPage').then((m) => ({ default: m.AdminModerationPanelPage })));
const UserManagementPage = lazy(() => import('./pages/admin/UserManagementPage').then((m) => ({ default: m.UserManagementPage })));
const AIMetricsDashboardPage = lazy(() => import('./pages/admin/AIMetricsDashboardPage').then((m) => ({ default: m.AIMetricsDashboardPage })));
const ThreatIntelDashboardPage = lazy(() => import('./pages/admin/ThreatIntelDashboardPage').then((m) => ({ default: m.ThreatIntelDashboardPage })));
const SystemHealthPage = lazy(() => import('./pages/admin/SystemHealthPage').then((m) => ({ default: m.SystemHealthPage })));
const AuditLogsPage = lazy(() => import('./pages/admin/AuditLogsPage').then((m) => ({ default: m.AuditLogsPage })));
const NotificationCenterPage = lazy(() => import('./pages/admin/NotificationCenterPage').then((m) => ({ default: m.NotificationCenterPage })));
const ExportCenterPage = lazy(() => import('./pages/admin/ExportCenterPage').then((m) => ({ default: m.ExportCenterPage })));
const EnterpriseSettingsPage = lazy(() => import('./pages/admin/EnterpriseSettingsPage').then((m) => ({ default: m.EnterpriseSettingsPage })));
const DeveloperPortalPage = lazy(() => import('./pages/developer/DeveloperPortalPage').then((m) => ({ default: m.DeveloperPortalPage })));
const APIAnalyticsPage = lazy(() => import('./pages/developer/APIAnalyticsPage').then((m) => ({ default: m.APIAnalyticsPage })));
const APIPlaygroundPage = lazy(() => import('./pages/developer/APIPlaygroundPage').then((m) => ({ default: m.APIPlaygroundPage })));
const HistoryPage = lazy(() => import('./pages/HistoryPage').then((m) => ({ default: m.HistoryPage })));
const AnalyticsPage = lazy(() => import('./pages/AnalyticsPage').then((m) => ({ default: m.AnalyticsPage })));
const ReportsPage = lazy(() => import('./pages/ReportsPage').then((m) => ({ default: m.ReportsPage })));
const ProfilePage = lazy(() => import('./pages/ProfilePage').then((m) => ({ default: m.ProfilePage })));
const SettingsPage = lazy(() => import('./pages/SettingsPage').then((m) => ({ default: m.SettingsPage })));
const NotFoundPage = lazy(() => import('./pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })));

// Authentication Pages
const LoginPage = lazy(() => import('./pages/auth/LoginPage').then((m) => ({ default: m.LoginPage })));
const RegisterPage = lazy(() => import('./pages/auth/RegisterPage').then((m) => ({ default: m.RegisterPage })));
const ForgotPasswordPage = lazy(() => import('./pages/auth/ForgotPasswordPage').then((m) => ({ default: m.ForgotPasswordPage })));
const ResetPasswordPage = lazy(() => import('./pages/auth/ResetPasswordPage').then((m) => ({ default: m.ResetPasswordPage })));
const VerifyEmailPage = lazy(() => import('./pages/auth/VerifyEmailPage').then((m) => ({ default: m.VerifyEmailPage })));

/**
 * GuardianAI Master App Component & Route Provider Stack
 */
export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <AccessibilityProvider>
          <ToastProvider>
            <AuthProvider>
              <CinematicMatrix3DCanvas />
              <BrowserRouter>
                <Suspense fallback={<LoadingSpinner fullPage label="Loading GuardianAI Platform..." />}>
                  <Routes>
                    {/* Standalone Authentication Pages */}
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                    <Route path="/reset-password" element={<ResetPasswordPage />} />
                    <Route path="/verify-email" element={<VerifyEmailPage />} />

                    {/* Main Application Shell Layout */}
                    <Route path="/" element={<MainLayout />}>
                      {/* Standalone Landing Page */}
                      <Route index element={<HomePage />} />

                      {/* Inspection Tools */}
                      <Route path="scan/message" element={<MessageScanPage />} />
                      <Route path="scan/email" element={<EmailScanPage />} />
                      <Route path="scan/url" element={<UrlScanPage />} />
                      <Route path="scan/qr" element={<QrScanPage />} />
                      <Route path="scan/result/:scanId" element={<ScanResultPage />} />

                      {/* Protected User Features (Requires Sign In) */}
                      <Route path="dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
                      <Route path="community" element={<ProtectedRoute><CommunityDashboardPage /></ProtectedRoute>} />
                      <Route path="history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
                      <Route path="analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
                      <Route path="reports" element={<ProtectedRoute><ReportsPage /></ProtectedRoute>} />
                      <Route path="profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
                      <Route path="settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />

                      {/* Developer Platform Routes */}
                      <Route path="developer" element={<ProtectedRoute><DeveloperPortalPage /></ProtectedRoute>} />
                      <Route path="developer/analytics" element={<ProtectedRoute><APIAnalyticsPage /></ProtectedRoute>} />
                      <Route path="developer/playground" element={<ProtectedRoute><APIPlaygroundPage /></ProtectedRoute>} />

                      {/* Admin Platform Routes */}
                      <Route path="admin/moderation" element={<ProtectedRoute><AdminModerationPanelPage /></ProtectedRoute>} />
                      <Route path="admin/users" element={<ProtectedRoute><UserManagementPage /></ProtectedRoute>} />
                      <Route path="admin/ai-usage" element={<ProtectedRoute><AIMetricsDashboardPage /></ProtectedRoute>} />
                      <Route path="admin/threat-intel" element={<ProtectedRoute><ThreatIntelDashboardPage /></ProtectedRoute>} />
                      <Route path="admin/system-health" element={<ProtectedRoute><SystemHealthPage /></ProtectedRoute>} />
                      <Route path="admin/audit-logs" element={<ProtectedRoute><AuditLogsPage /></ProtectedRoute>} />
                      <Route path="admin/notifications" element={<ProtectedRoute><NotificationCenterPage /></ProtectedRoute>} />
                      <Route path="admin/export" element={<ProtectedRoute><ExportCenterPage /></ProtectedRoute>} />
                      <Route path="admin/master-settings" element={<ProtectedRoute><EnterpriseSettingsPage /></ProtectedRoute>} />

                      <Route path="*" element={<NotFoundPage />} />
                    </Route>
                  </Routes>
                </Suspense>
              </BrowserRouter>
            </AuthProvider>
          </ToastProvider>
        </AccessibilityProvider>
      </ErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
