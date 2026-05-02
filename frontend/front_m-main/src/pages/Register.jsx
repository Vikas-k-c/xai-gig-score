import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, ArrowRight, Loader2 } from 'lucide-react';
import { apiRequest } from '../lib/api';
import { saveToken } from '../lib/auth';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });
      saveToken(data.access_token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#fcf8fa] min-h-screen flex items-center justify-center p-6 antialiased">
      <main className="w-full max-w-[440px]">
        <div className="flex flex-col items-center justify-center mb-10">
          <div className="flex items-center gap-2 mb-1">
            <Shield className="text-black" size={32} strokeWidth={2.5} />
            <span className="text-2xl font-black tracking-tight">GigRisk</span>
          </div>
          <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-gray-400">Institutional Trust</span>
        </div>

        <div className="bg-white border border-gray-100 rounded-2xl shadow-[0_4px_24px_rgba(0,0,0,0.03)] overflow-hidden">
          <div className="h-1.5 w-full bg-black"></div>
          <div className="p-10">
            <div className="mb-8">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">Create Account</h1>
              <p className="text-sm text-gray-500">Initialize your risk analyst profile.</p>
            </div>

            {error && (
              <div className="bg-red-50 text-red-600 text-xs p-4 rounded-lg mb-6 border border-red-100 font-medium">
                {error}
              </div>
            )}

            <form onSubmit={handleRegister} className="flex flex-col gap-5">
              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="name">Full Name</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all" 
                  id="name" 
                  placeholder="Jane Doe" 
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required 
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="email">Email Address</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all" 
                  id="email" 
                  placeholder="jane@institution.com" 
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required 
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-bold uppercase tracking-wider text-gray-900" htmlFor="password">Password</label>
                <input 
                  className="bg-gray-50 border border-gray-100 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-300 transition-all" 
                  id="password" 
                  placeholder="••••••••" 
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required 
                />
              </div>

              <div className="mt-4">
                <button 
                  className="w-full bg-black text-white font-bold rounded-lg py-4 flex items-center justify-center gap-2 hover:bg-gray-800 transition-all shadow-xl shadow-black/5 active:scale-[0.98] disabled:opacity-50"
                  type="submit"
                  disabled={loading}
                >
                  {loading ? <Loader2 className="animate-spin" size={20} /> : 'Create Account'}
                  {!loading && <ArrowRight size={18} />}
                </button>
              </div>
            </form>
          </div>
          <div className="bg-gray-50 border-t border-gray-100 p-6 text-center">
            <p className="text-sm text-gray-500">
              Already registered? 
              <Link className="text-black font-bold hover:underline ml-2" to="/login">Login instead</Link>
            </p>
          </div>
        </div>
        
        <p className="mt-8 text-center text-[10px] text-gray-400 font-medium px-10">
          By creating an account, you agree to our Terms of Service and Privacy Policy. Securely encrypted.
        </p>
      </main>
    </div>
  );
}
