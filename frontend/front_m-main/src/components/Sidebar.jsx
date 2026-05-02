import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Share2, 
  ShieldCheck, 
  CreditCard, 
  HelpCircle, 
  LogOut 
} from 'lucide-react';
import { removeToken } from '../lib/auth';
import { cn } from '../lib/utils';

export default function Sidebar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Platform Sync', icon: Share2, path: '/connect' },
    { name: 'Risk Factors', icon: ShieldCheck, path: '/predict' },
    { name: 'Loan Status', icon: CreditCard, path: '/loans' },
  ];

  return (
    <aside className="bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 fixed left-0 top-0 h-screen w-64 border-r border-gray-100 dark:border-gray-800 flex flex-col p-4 space-y-6 z-20">
      <div className="px-2">
        <h1 className="text-xl font-black text-gray-900 dark:text-gray-100 mb-1">GigRisk</h1>
        <p className="text-gray-500 uppercase tracking-widest text-[10px] font-semibold">Institutional Trust</p>
      </div>

      <nav className="flex-1 space-y-2 mt-8">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => cn(
              "flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200 duration-150 active:translate-x-1",
              isActive 
                ? "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white font-bold" 
                : "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-900/50"
            )}
          >
            <item.icon size={20} />
            <span className="font-medium">{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="space-y-2 border-t border-gray-100 dark:border-gray-800 pt-4">
        <button className="w-full flex items-center gap-3 text-gray-500 dark:text-gray-400 px-4 py-2.5 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-all rounded-lg active:translate-x-1">
          <HelpCircle size={20} />
          <span className="font-medium text-sm">Help Center</span>
        </button>
        <button 
          onClick={handleLogout}
          className="w-full flex items-center gap-3 text-gray-500 dark:text-gray-400 px-4 py-2.5 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-all rounded-lg active:translate-x-1"
        >
          <LogOut size={20} />
          <span className="font-medium text-sm">Logout</span>
        </button>
      </div>
    </aside>
  );
}
