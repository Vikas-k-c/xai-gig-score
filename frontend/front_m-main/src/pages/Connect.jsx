import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  CheckCircle2, 
  Loader2, 
  PlusCircle, 
  Briefcase,
  Layers,
  ArrowRight
} from 'lucide-react';
import { apiRequest } from '../lib/api';
import DashboardLayout from '../components/DashboardLayout';

export default function ConnectPage() {
  const [connected, setConnected] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(null);

  const platforms = [
    { platformId: 'uber',        name: 'Uber',   icon: Briefcase, color: 'bg-black text-white' },
    { platformId: 'zomato',      name: 'Zomato', icon: Briefcase, color: 'bg-red-600 text-white' },
    { platformId: 'swiggy',      name: 'Swiggy', icon: Briefcase, color: 'bg-orange-500 text-white' },
    { platformId: 'rapido',      name: 'Rapido', icon: Briefcase, color: 'bg-yellow-400 text-black' },
    { platformId: 'upwork',      name: 'Upwork', icon: Briefcase, color: 'bg-green-600 text-white' },
    { platformId: 'ola',         name: 'Ola',    icon: Briefcase, color: 'bg-lime-500 text-black' },
  ];

  useEffect(() => {
    fetchConnected();
  }, []);

  const fetchConnected = async () => {
    try {
      const data = await apiRequest('/platforms/');
      setConnected(data.map(p => p.platform_name));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = async (platformId) => {
    setConnecting(platformId);
    try {
      await apiRequest('/platforms/connect', {
        method: 'POST',
        body: JSON.stringify({ platform_name: platformId }),
      });
      setConnected(prev => [...prev, platformId]);
    } catch (err) {
      alert(err.message);
    } finally {
      setConnecting(null);
    }
  };

  return (
    <DashboardLayout>
      <div className="mb-10">
        <h1 className="text-3xl font-black text-gray-900 mb-1">Platform Integration</h1>
        <p className="text-gray-500 text-lg">Connect your gig profiles to build a comprehensive earning history.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {platforms.map((platform) => {
          const isConnected = connected.includes(platform.platformId);
          const isConnecting = connecting === platform.platformId;

          return (
            <div 
              key={platform.platformId} 
              className={`bg-white rounded-2xl p-8 border border-gray-100 shadow-[0_4px_12px_rgba(0,0,0,0.03)] flex items-center justify-between transition-all hover:shadow-xl hover:shadow-black/[0.02] ${isConnected ? 'opacity-100' : 'opacity-80'}`}
            >
              <div className="flex items-center gap-5">
                <div className={`w-14 h-14 rounded-xl ${platform.color} flex items-center justify-center shadow-lg font-black text-xl`}>
                  {platform.name[0]}
                </div>
                <div>
                  <h3 className="text-xl font-black text-gray-900 leading-tight">{platform.name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    {isConnected ? (
                      <>
                        <span className="w-2 h-2 rounded-full bg-green-500"></span>
                        <span className="text-[10px] font-black uppercase tracking-widest text-green-600">Active</span>
                      </>
                    ) : (
                      <>
                        <span className="w-2 h-2 rounded-full bg-gray-200"></span>
                        <span className="text-[10px] font-black uppercase tracking-widest text-gray-400">Disconnected</span>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {isConnected ? (
                <button className="text-[10px] font-black uppercase tracking-widest px-5 py-2.5 rounded-lg border border-gray-100 bg-gray-50 text-gray-400 cursor-not-allowed">
                  Syncing
                </button>
              ) : (
                <button 
                  onClick={() => handleConnect(platform.platformId)}
                  disabled={isConnecting}
                  className="text-[10px] font-black uppercase tracking-widest px-5 py-2.5 rounded-lg bg-black text-white hover:bg-gray-800 transition-all shadow-xl shadow-black/5 flex items-center"
                >
                  {isConnecting ? <Loader2 className="animate-spin" size={14} /> : 'Connect'}
                </button>
              )}
            </div>
          );
        })}
      </div>

      <div className="mt-16 p-10 bg-gray-900 rounded-3xl text-white flex flex-col sm:flex-row items-center justify-between gap-8">
        <div className="space-y-2">
          <h3 className="text-2xl font-black">Missing a Platform?</h3>
          <p className="text-gray-400 font-medium">We're constantly adding new integrations to improve scoring precision.</p>
        </div>
        <button className="bg-white text-black px-8 py-3 rounded-xl font-bold flex items-center gap-2 hover:bg-gray-100 transition-all active:scale-95 text-sm whitespace-nowrap">
          Request Integration
          <PlusCircle size={18} />
        </button>
      </div>
    </DashboardLayout>
  );
}
