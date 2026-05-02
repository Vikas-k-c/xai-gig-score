import React, { useState, useEffect } from 'react';
import { 
  BadgeCheck, 
  Hourglass, 
  Search, 
  Loader2, 
  ShieldCheck, 
  Tag, 
  AlertCircle 
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function PANPage() {
  const [pan, setPan] = useState('');
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const data = await apiRequest('/pan/');
      setStatus(data);
    } catch (err) {
      // Optional: ignore 404 if no PAN submitted yet
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (pan.length !== 10) return;
    
    setSubmitting(true);
    setError(null);
    
    try {
      const data = await apiRequest('/pan/submit', {
        method: 'POST',
        body: JSON.stringify({ pan_number: pan.toUpperCase() }),
      });
      setStatus(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="animate-spin text-gray-400" size={40} />
      </div>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-[500px] mx-auto mt-12">
        <div className="bg-white rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.06)] border border-gray-100 overflow-hidden">
          <div className="p-10 flex flex-col items-center text-center">
            <div className="w-16 h-16 rounded-full bg-gray-50 flex items-center justify-center border border-gray-100 mb-6">
              <ShieldCheck className="text-black" size={32} />
            </div>
            
            <h1 className="text-2xl font-black text-gray-900 mb-2">Identity Verification</h1>
            <p className="text-sm text-gray-500 mb-8 px-4">
              Please provide your 10-digit Permanent Account Number for institutional risk assessment calibration.
            </p>

            {error && (
              <div className="w-full bg-red-50 text-red-600 text-xs p-4 rounded-lg mb-6 border border-red-100 font-medium text-left">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="w-full space-y-6">
              <div className="flex flex-col gap-2 text-left">
                <div className="flex justify-between items-end">
                  <label className="text-[10px] font-black uppercase tracking-widest text-black" htmlFor="pan">PAN Number</label>
                  <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">10 Characters</span>
                </div>
                <div className="relative">
                  <input 
                    className="w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-3.5 font-mono text-lg tracking-wider focus:outline-none focus:border-black focus:ring-1 focus:ring-gray-300 transition-all uppercase placeholder:text-gray-300" 
                    id="pan" 
                    maxLength={10} 
                    placeholder="ABCDE1234F" 
                    type="text"
                    value={pan}
                    onChange={(e) => setPan(e.target.value.toUpperCase())}
                    disabled={status?.is_verified}
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                    <Tag className="text-gray-300" size={20} />
                  </div>
                </div>
              </div>

              {!status?.is_verified && (
                <button 
                  className="w-full bg-black text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-800 transition-all active:scale-[0.98] disabled:opacity-50 shadow-xl shadow-black/10"
                  type="submit"
                  disabled={submitting || pan.length !== 10}
                >
                  {submitting ? <Loader2 className="animate-spin" size={20} /> : 'Verify Identity'}
                  {!submitting && <BadgeCheck size={20} />}
                </button>
              )}
            </form>

            <div className="w-full h-px bg-gray-50 my-8"></div>

            <div className="flex flex-col items-center gap-3">
              <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Verification Status</span>
              {status?.is_verified ? (
                <div className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-green-50 border border-green-100 shadow-sm shadow-green-100/50">
                  <BadgeCheck size={18} className="text-green-600" />
                  <span className="text-xs font-black text-green-700 uppercase tracking-widest">Identity Verified</span>
                </div>
              ) : (
                <div className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-gray-100 border border-gray-200">
                  <Hourglass size={18} className="text-gray-500 animate-pulse" />
                  <span className="text-xs font-black text-gray-900 uppercase tracking-widest">
                    {status ? 'Submission Pending' : 'Awaiting Input'}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
