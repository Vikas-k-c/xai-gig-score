import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthGuard from './components/AuthGuard';

// Pages
import LandingPage from './pages/Landing';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import Dashboard from './pages/Dashboard';
import PANPage from './pages/PAN';
import ConnectPage from './pages/Connect';
import PredictPage from './pages/Predict';
import LoansPage from './pages/Loans';

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected Routes */}
        <Route 
          path="/dashboard" 
          element={
            <AuthGuard>
              <Dashboard />
            </AuthGuard>
          } 
        />
        <Route 
          path="/pan" 
          element={
            <AuthGuard>
              <PANPage />
            </AuthGuard>
          } 
        />
        <Route 
          path="/connect" 
          element={
            <AuthGuard>
              <ConnectPage />
            </AuthGuard>
          } 
        />
        <Route 
          path="/predict" 
          element={
            <AuthGuard>
              <PredictPage />
            </AuthGuard>
          } 
        />
        <Route 
          path="/loans" 
          element={
            <AuthGuard>
              <LoansPage />
            </AuthGuard>
          } 
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
