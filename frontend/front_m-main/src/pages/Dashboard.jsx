import React, { useState, useEffect } from 'react';
import { 
  CheckCircle, 
  TrendingDown, 
  Wallet, 
  Star, 
  ArrowUpRight,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const response = await apiRequest('/dashboard/');
        setData(response);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
        <AlertCircle className="text-red-500 mb-4" size={48} />
        <h2 className="text-xl font-bold text-gray-900 mb-2">Sync Failed</h2>
        <p className="text-gray-500 max-w-md">{error}</p>
        <button 
          onClick={() => window.location.reload()}
          className="mt-6 px-6 py-2 bg-black text-white rounded-lg font-bold"
        >
          Retry Calibration
        </button>
      </div>
    );
  }

  const { user, platform_summary, latest_prediction, loans, prediction_history } = data;

  return (
    <DashboardLayout user={user}>
      <div className="mb-8">
        <h2 className="text-3xl font-black text-gray-900 mb-1">Platform Overview</h2>
        <p className="text-gray-500 text-lg">Comprehensive credit risk evaluation based on aggregated gig platform data.</p>
      </div>

      <div className="grid grid-cols-12 gap-6 mb-12">
        {/* Credit Score Card */}
        <div className="col-span-12 lg:col-span-4 bg-white rounded-2xl p-8 border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-2">GigRisk Credit Score</p>
            <div className="flex items-baseline gap-2 mb-6">
              <h3 className="text-6xl font-black text-black">
                {latest_prediction?.credit_score ? Math.round(latest_prediction.credit_score) : '—'}
              </h3>
              <span className="text-sm font-semibold text-gray-400">/ 850</span>
            </div>
          </div>
          <div>
            <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
              <div 
                className="h-full bg-black rounded-full transition-all duration-1000" 
                style={{ width: `${(latest_prediction?.credit_score / 850) * 100 || 0}%` }}
              ></div>
            </div>
            <div className="flex justify-between mt-3">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Poor</span>
              <span className="text-[10px] font-bold text-black uppercase tracking-wider">Excellent</span>
            </div>
          </div>
        </div>

        {/* Risk & Probability Card */}
        <div className="col-span-12 lg:col-span-4 bg-white rounded-2xl p-8 border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div className="space-y-6">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-2">Calculated Risk Level</p>
              <div className={`inline-flex items-center px-4 py-1.5 rounded-full ${
                latest_prediction?.risk_level === 'High' ? 'bg-red-50 text-red-600' : 'bg-gray-100 text-gray-900'
              }`}>
                <CheckCircle size={14} className="mr-2" />
                <span className="text-[10px] font-bold uppercase tracking-widest leading-none">
                  {latest_prediction?.risk_level || 'Pending Assessment'}
                </span>
              </div>
            </div>
            
            <div className="pt-6 border-t border-gray-50">
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-2">Default Probability</p>
              <div className="flex items-center gap-3">
                <span className="text-3xl font-black text-gray-900">
                  {latest_prediction?.default_probability ? (latest_prediction.default_probability * 100).toFixed(1) : '0.0'}%
                </span>
                <TrendingDown className="text-gray-400" size={24} />
              </div>
              <p className="text-xs text-gray-500 mt-2 font-medium">Based on multi-platform history</p>
            </div>
          </div>
        </div>

        {/* Aggregated Metrics Card */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-4">
          <div className="flex-1 bg-white rounded-2xl p-6 border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.03)] flex items-center justify-between">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1">Monthly Avg Income</p>
              <p className="text-2xl font-black text-black">₹{platform_summary?.avg_income?.toLocaleString() || '0'}</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-gray-50 flex items-center justify-center text-gray-900">
              <Wallet size={24} />
            </div>
          </div>

          <div className="flex-1 bg-white rounded-2xl p-6 border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.03)] flex items-center justify-between">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1">Avg Platform Rating</p>
              <div className="flex items-baseline gap-1">
                <p className="text-2xl font-black text-black">{platform_summary?.avg_rating?.toFixed(1) || '0.0'}</p>
                <span className="text-[10px] font-bold text-gray-400">/ 5.0</span>
              </div>
            </div>
            <div className="h-12 w-12 rounded-full bg-gray-50 flex items-center justify-center text-gray-900">
              <Star size={24} />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Recent Loan Activity */}
        <div className="col-span-12 lg:col-span-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Active Credit Lines</h3>
            <button className="text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-black">View All</button>
          </div>
          
          <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
            {loans?.length > 0 ? (
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-100">
                    <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">Institution</th>
                    <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">Allocated</th>
                    <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">Date</th>
                    <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {loans.slice(0, 5).map((loan, idx) => (
                    <tr key={idx} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors">
                      <td className="py-5 px-6">
                         <span className="font-bold text-gray-900">{loan.bank_name}</span>
                      </td>
                      <td className="py-5 px-6 font-bold text-gray-900">₹{loan.amount?.toLocaleString()}</td>
                      <td className="py-5 px-6 text-sm text-gray-500">{new Date(loan.created_at).toLocaleDateString()}</td>
                      <td className="py-5 px-6 text-right">
                        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-100 text-gray-900 text-[10px] font-bold uppercase tracking-wider">
                          Active
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="p-12 text-center">
                <p className="text-gray-400 text-sm font-medium">No active credit lines found.</p>
              </div>
            )}
          </div>
        </div>

        {/* Prediction Stats */}
        <div className="col-span-12 lg:col-span-4">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Impact Analysis</h3>
          <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden">
             <div className="p-6 border-b border-gray-50 bg-gray-50/50">
               <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Positive Drivers</p>
               <div className="space-y-3">
                 {latest_prediction?.positive_factors?.map((factor, i) => (
                   <div key={i} className="flex gap-2 text-xs text-gray-600 font-medium">
                     <span className="text-black">•</span>
                     <span>{factor}</span>
                   </div>
                 ))}
                 {!latest_prediction?.positive_factors?.length && <p className="text-xs text-gray-400">No positive factors detected.</p>}
               </div>
             </div>
             <div className="p-6">
               <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Risk Constraints</p>
               <div className="space-y-3">
                 {latest_prediction?.negative_factors?.map((factor, i) => (
                   <div key={i} className="flex gap-2 text-xs text-red-500 font-medium">
                     <span className="text-red-500">•</span>
                     <span>{factor}</span>
                   </div>
                 ))}
                 {!latest_prediction?.negative_factors?.length && <p className="text-xs text-gray-400">No risk constraints detected.</p>}
               </div>
             </div>
          </div>
        </div>
      </div>

      {/* Score History */}
      {prediction_history?.length > 0 && (
        <div className="mt-12">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Score History</h3>
          <div className="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-100">
                  <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">#</th>
                  <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">Credit Score</th>
                  <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400">Risk Level</th>
                  <th className="py-4 px-6 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Date</th>
                </tr>
              </thead>
              <tbody>
                {prediction_history.map((p, idx) => (
                  <tr key={p.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors">
                    <td className="py-4 px-6 text-xs font-bold text-gray-400">{idx + 1}</td>
                    <td className="py-4 px-6 font-black text-gray-900">{Math.round(p.credit_score)}</td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
                        p.risk_level === 'High' ? 'bg-red-50 text-red-600' :
                        p.risk_level === 'Medium' ? 'bg-yellow-50 text-yellow-700' :
                        'bg-green-50 text-green-700'
                      }`}>
                        {p.risk_level}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-sm text-gray-500 text-right">
                      {new Date(p.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
