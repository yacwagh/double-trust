import React from 'react';
import Navigation from './Navigation';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <Navigation />
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;
