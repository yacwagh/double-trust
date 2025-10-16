import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/agents', label: 'Agents', icon: '🤖' },
    { path: '/discovery', label: 'Discovery', icon: '🔍' },
  ];

  return (
    <nav className="w-64 bg-gray-900 text-white min-h-screen p-6">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-white">DoubleTrust</h1>
        <p className="text-gray-400 text-sm">Agent & Tools Governance</p>
      </div>
      
      <ul className="space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="font-medium">{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
};

export default Navigation;
