import React, { useState } from 'react';
import { 
  Zap, 
  TrendingUp, 
  TrendingDown, 
  Loader2, 
  ShieldCheck, 
  AlertTriangle,
  History,
  ArrowRight,
  Target
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function PredictPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runPrediction = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiRequest('/predict/', { method: 'POST' });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Risk Calibration</h1>
        <p className="text-gray-500 text-lg">Run our neural engine to calculate your real-time GigRisk Score™.</p>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Control Card */}
        <div className="col-span-12 lg:col-span-5">
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-[0_8px_32px_rgba(0,0,0,0.04)] h-full flex flex-col">
            <div className="w-16 h-16 rounded-2xl bg-black text-white flex items-center justify-center mb-8 shadow-2xl shadow-black/20">
              <Zap size={32} fill="white" />
            </div>

            <h2 className="text-2xl font-black text-gray-900 mb-4">Initial Calibration</h2>
            <p className="text-gray-500 font-medium mb-10 leading-relaxed">
              Our algorithm analyzes over 40 variables across your connected platforms including payout consistency, customer sentiment, and operational tenure.
            </p>

            <div className="space-y-4 mb-12">
              {[
                'Verifying platform credentials...',
                'Fetching 12-month historical data...',
                'Analyzing income volatility...',
                'Correlating cross-platform behavior...'
              ].map((step, i) => (
                <div key={i} className="flex items-center gap-3 text-xs font-bold text-gray-400 uppercase tracking-widest">
                  <div className="w-1.5 h-1.5 rounded-full bg-gray-200"></div>
                  {step}
                </div>
              ))}
            </div>

            <button 
              onClick={runPrediction}
              disabled={loading}
              className="mt-auto w-full bg-black text-white font-black py-4 rounded-xl flex items-center justify-center gap-3 hover:bg-gray-800 transition-all shadow-2xl shadow-black/10 active:scale-[0.98] disabled:opacity-50"
            >
              {loading ? <Loader2 className="animate-spin" size={20} /> : <Target size={20} />}
              {loading ? 'Processing Engine...' : 'Run Analysis Engine'}
            </button>
          </div>
        </div>

        {/* Results Area */}
        <div className="col-span-12 lg:col-span-7">
          {error && (
            <div className="bg-red-50 text-red-600 p-6 rounded-2xl border border-red-100 flex items-start gap-4 shadow-sm mb-6">
              <AlertTriangle className="shrink-0" size={24} />
              <div>
                <h4 className="font-black text-sm uppercase tracking-widest mb-1">System Error</h4>
                <p className="text-sm font-medium">{error}</p>
              </div>
            </div>
          )}

          {result ? (
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
                  <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Projected Score</p>
                  <div className="text-5xl font-black text-black mb-1">{Math.round(result.credit_score)}</div>
                  <p className="text-xs font-bold text-green-600 uppercase tracking-widest">Excellent Rating</p>
                </div>
                <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
                  <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-4">Risk Magnitude</p>
                  <div className="text-3xl font-black text-black h-[50px] flex items-end pb-1">{result.risk_level}</div>
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest">Calculated Level</p>
                </div>
              </div>

              <div className="bg-white rounded-3xl border border-gray-100 overflow-hidden shadow-sm">
                <div className="p-8 border-b border-gray-50 bg-gray-50/50">
                  <div className="flex items-center gap-2 mb-6">
                    <TrendingUp className="text-black" size={20} />
                    <h4 className="text-sm font-black uppercase tracking-widest text-gray-900 underline decoration-black decoration-2">Positive Drivers</h4>
                  </div>
                  <div className="grid grid-cols-1 gap-4">
                    {result.positive_factors.map((f, i) => (
                      <div key={i} className="bg-white p-4 rounded-xl border border-gray-100 text-xs font-bold text-gray-600 leading-relaxed shadow-sm">
                        {f}
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="p-8">
                  <div className="flex items-center gap-2 mb-6">
                    <TrendingDown className="text-red-500" size={20} />
                    <h4 className="text-sm font-black uppercase tracking-widest text-red-600">Risk Constraints</h4>
                  </div>
                  <div className="grid grid-cols-1 gap-4">
                    {result.negative_factors.map((f, i) => (
                      <div key={i} className="bg-red-50/30 p-4 rounded-xl border border-red-50 text-xs font-bold text-red-800 leading-relaxed">
                        {f}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-gray-100 border-dashed p-20 flex flex-col items-center justify-center text-center">
              <History size={48} className="text-gray-200 mb-6" />
              <p className="text-gray-400 font-bold uppercase tracking-[0.2em] text-xs">Awaiting Analysis</p>
              <p className="text-gray-300 text-sm mt-2 max-w-xs">Run the engine to populate your real-time risk intelligence factors.</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
