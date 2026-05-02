import React, { useState, useEffect } from 'react';
import { 
  Landmark, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  ArrowRight, 
  Loader2,
  Building2,
  BadgePercent
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function LoansPage() {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [bankName, setBankName] = useState('');
  const [amount, setAmount] = useState('');

  const offers = [
    { bank: 'HDFC Bank', amount: '1,50,000', apr: '8.5%', match: 'Excellent Match' },
    { bank: 'ICICI Bank', amount: '2,00,000', apr: '9.2%', match: 'Good Match' },
    { bank: 'IDFC First', amount: '50,000', apr: '10.5%', match: 'Fair Match' },
  ];

  useEffect(() => {
    fetchLoans();
  }, []);

  const fetchLoans = async () => {
    try {
      const data = await apiRequest('/loans/');
      setLoans(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await apiRequest('/loans/apply', {
        method: 'POST',
        body: JSON.stringify({ bank_name: bankName, amount: parseFloat(amount) }),
      });
      setBankName('');
      setAmount('');
      fetchLoans();
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Credit Liquidity</h1>
        <p className="text-gray-500 text-lg">Select and deploy institutional credit lines based on your GigRisk profile.</p>
      </div>

      {/* Offers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {offers.map((offer, i) => (
          <div key={i} className="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm flex flex-col justify-between hover:shadow-xl hover:shadow-black/[0.02] transition-all">
            <div>
              <div className="flex justify-between items-start mb-6">
                <div className="w-12 h-12 rounded-xl bg-gray-50 flex items-center justify-center border border-gray-100">
                  <Landmark className="text-black" size={24} />
                </div>
                <span className="text-[10px] font-black uppercase tracking-widest px-3 py-1 bg-gray-100 rounded-full text-gray-900">
                  {offer.match}
                </span>
              </div>
              <h3 className="text-xl font-black text-black mb-1">{offer.bank}</h3>
              <p className="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-6">Pre-approved Amount</p>
              <div className="text-4xl font-black text-black mb-2">₹{offer.amount}</div>
              <p className="text-xs font-bold text-gray-900">APR starting at {offer.apr}</p>
            </div>
            
            <button 
              onClick={() => {
                setBankName(offer.bank);
                setAmount(offer.amount.replace(/,/g, ''));
              }}
              className="mt-8 w-full bg-black text-white font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-800 transition-all active:scale-[0.98]"
            >
              Fast Apply
              <ArrowRight size={18} />
            </button>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Apply Form */}
        <div className="col-span-12 lg:col-span-4">
          <div className="bg-white rounded-3xl p-10 border border-gray-100 shadow-sm h-full">
            <h3 className="text-xl font-black text-gray-900 mb-8 border-b border-gray-50 pb-4">New Request</h3>
            <form onSubmit={handleApply} className="space-y-6">
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Target Institution</label>
                <div className="relative">
                  <input 
                    className="w-full bg-gray-50 border border-gray-100 rounded-xl px-10 py-3.5 text-sm font-bold focus:outline-none focus:border-black transition-all"
                    placeholder="e.g. HDFC Bank"
                    value={bankName}
                    onChange={(e) => setBankName(e.target.value)}
                    required
                  />
                  <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-gray-400">Request Amount (INR)</label>
                <div className="relative">
                  <input 
                    className="w-full bg-gray-50 border border-gray-100 rounded-xl px-10 py-3.5 text-sm font-black focus:outline-none focus:border-black transition-all"
                    placeholder="1,00,000"
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                  />
                  <BadgePercent className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                </div>
              </div>
              <button 
                className="w-full bg-black text-white font-black py-4 rounded-xl flex items-center justify-center gap-2 hover:bg-gray-800 transition-all disabled:opacity-50 mt-10 shadow-2xl shadow-black/10"
                type="submit"
                disabled={submitting}
              >
                {submitting ? <Loader2 className="animate-spin" size={20} /> : 'Process Disbursement'}
              </button>
            </form>
          </div>
        </div>

        {/* Loan History */}
        <div className="col-span-12 lg:col-span-8">
          <h3 className="text-xl font-black text-gray-900 mb-8 px-2 flex items-center justify-between">
            Active Disbursements
            <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">{loans.length} Total</span>
          </h3>
          <div className="bg-white border border-gray-100 rounded-3xl overflow-hidden shadow-sm">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50/50 border-b border-gray-100">
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Institution</th>
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400">Amount</th>
                  <th className="py-4 px-8 text-[10px] font-black uppercase tracking-widest text-gray-400 text-right">Status</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                   <tr>
                     <td colSpan="3" className="py-20 text-center">
                        <Loader2 className="animate-spin inline-block text-gray-300" size={32} />
                     </td>
                   </tr>
                ) : loans.length > 0 ? (
                  loans.map((loan, idx) => (
                    <tr key={idx} className="border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors">
                      <td className="py-6 px-8 font-black text-gray-900">{loan.bank_name}</td>
                      <td className="py-6 px-8 font-black text-gray-900">₹{loan.amount?.toLocaleString()}</td>
                      <td className="py-6 px-8 text-right">
                        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-green-50 text-green-700 text-[10px] font-black uppercase tracking-widest border border-green-100">
                          <CheckCircle2 size={12} />
                          Active
                        </div>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="py-24 text-center px-8">
                       <p className="text-gray-400 text-sm font-bold uppercase tracking-widest">No active disbursements</p>
                       <p className="text-gray-300 text-xs mt-2 font-medium">Your historical credit activity will appear here once finalized.</p>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
