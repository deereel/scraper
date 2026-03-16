import React from 'react';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-primary-600">BeScraped</h1>
              </div>
              <nav className="hidden md:ml-6 md:flex md:space-x-8">
                <Link href="/" className="text-gray-500 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Home
                </Link>
                <Link href="/dashboard" className="text-gray-500 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link href="/docs" className="text-gray-500 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Docs
                </Link>
              </nav>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {children}
      </main>

      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-lg font-semibold mb-4">BeScraped</h3>
                <p className="text-gray-600 text-sm">
                  Automatic company information extraction from public sources.
                </p>
              </div>
              <div>
                <h4 className="text-md font-medium mb-4">Legal</h4>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link href="/privacy" className="text-gray-500 hover:text-primary-600">
                      Privacy Policy
                    </Link>
                  </li>
                  <li>
                    <Link href="/terms" className="text-gray-500 hover:text-primary-600">
                      Terms of Service
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="text-md font-medium mb-4">Resources</h4>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link href="/docs" className="text-gray-500 hover:text-primary-600">
                      Documentation
                    </Link>
                  </li>
                  <li>
                    <Link href="/api" className="text-gray-500 hover:text-primary-600">
                      API Documentation
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
            <div className="mt-8 text-center text-sm text-gray-500">
              <p>© 2024 BeScraped. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
