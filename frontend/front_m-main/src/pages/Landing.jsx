import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, ArrowRight } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#fcf8fa] flex flex-col items-center justify-center p-6 antialiased">
      <main className="w-full max-w-4xl text-center">
        <div className="flex flex-col items-center justify-center mb-12">
          <div className="flex items-center gap-3 mb-2">
            <Shield className="text-black" size={40} strokeWidth={2.5} />
            <span className="text-4xl font-black tracking-tight">GigRisk</span>
          </div>
          <span className="text-xs font-bold uppercase tracking-[0.2em] text-gray-400">Institutional Trust Protocol</span>
        </div>

        <h1 className="text-5xl font-black tracking-tight text-gray-900 mb-6 sm:text-6xl leading-[1.1]">
          Decentralized Credit Scoring for the <span className="text-transparent bg-clip-text bg-gradient-to-r from-black to-gray-600">Gig Economy</span>
        </h1>
        
        <p className="text-xl text-gray-500 max-w-2xl mx-auto mb-10 leading-relaxed">
          Aggregated risk intelligence powered by platform data. Build your institutional profile and unlock financial opportunities.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link 
            to="/register" 
            className="w-full sm:w-auto bg-black text-white px-10 py-4 rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-gray-800 transition-all shadow-xl hover:shadow-black/10 active:scale-95"
          >
            Get Started
            <ArrowRight size={20} />
          </Link>
          <Link 
            to="/login" 
            className="w-full sm:w-auto bg-white border border-gray-200 text-black px-10 py-4 rounded-xl font-bold hover:bg-gray-50 transition-all active:scale-95"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-8 text-left max-w-3xl mx-auto">
          {[
            { title: 'Platform Sync', desc: 'Securely connect Uber, Zomato, Upwork and more.' },
            { title: 'Dynamic Prediction', desc: 'Real-time default probability and credit scoring.' },
            { title: 'Bank Connectivity', desc: 'Direct access to institutional credit lines.' }
          ].map((feature, i) => (
            <div key={i} className="space-y-2">
              <h3 className="font-bold text-gray-900 uppercase text-xs tracking-wider">{feature.title}</h3>
              <p className="text-sm text-gray-500">{feature.desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
