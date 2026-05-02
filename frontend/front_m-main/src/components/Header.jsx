import React from 'react';
import { Search, Bell, Settings } from 'lucide-react';

export default function Header({ user }) {
  return (
    <header className="bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 border-b border-gray-100 dark:border-gray-800 flex justify-between items-center h-16 px-6 w-full ml-64 max-w-[calc(100%-16rem)] z-10 sticky top-0">
      <div className="flex items-center">
        <div className="relative w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          <input 
            className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border-none rounded-md text-sm focus:ring-1 focus:ring-gray-300 dark:focus:ring-gray-700 transition-all outline-none" 
            placeholder="Search records..." 
            type="text" 
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors duration-200 p-2 rounded-full active:opacity-80">
          <Bell size={20} />
        </button>
        <button className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors duration-200 p-2 rounded-full active:opacity-80">
          <Settings size={20} />
        </button>
        
        <div className="flex items-center gap-3 ml-2 border-l pl-4 border-gray-100 dark:border-gray-800">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-bold leading-tight">{user?.name || 'Guest'}</p>
            <p className="text-[10px] text-gray-500 uppercase tracking-tighter">Gig Analyst</p>
          </div>
          <div className="h-8 w-8 rounded-full overflow-hidden bg-gray-100 border border-gray-200">
            <img 
              alt="Gig Worker User Profile" 
              className="w-full h-full object-cover" 
              src={`https://ui-avatars.com/api/?name=${user?.name || 'User'}&background=000&color=fff`}
            />
          </div>
        </div>
      </div>
    </header>
  );
}
