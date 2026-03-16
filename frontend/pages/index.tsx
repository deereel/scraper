import React from 'react';
import Layout from '../components/Layout';

const Home: React.FC = () => {
  return (
    <Layout>
      <div className="bg-white">
        {/* Hero Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
              Instant Company Data Extraction
            </h1>
            <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
              Extract company names, addresses and executives from websites, LinkedIn and official registries automatically.
            </p>
            <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <a
                href="/dashboard"
                className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-white bg-primary-600 hover:bg-primary-700 md:text-lg md:px-10 transition-colors duration-200"
              >
                Start Scraping
              </a>
              <a
                href="/docs"
                className="inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-full text-gray-700 bg-white hover:bg-gray-50 md:text-lg md:px-10 transition-colors duration-200"
              >
                Learn More
              </a>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-gray-50 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Powerful Features
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                BeScraped automates the process of collecting company information from multiple public sources.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="card">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 mb-4">
                    <svg className="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">Website Scraping</h3>
                  <p className="text-gray-600">
                    Automatically scrape company websites for information from about, contact, and team pages.
                  </p>
                </div>
              </div>

              <div className="card">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 mb-4">
                    <svg className="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">Executive Discovery</h3>
                  <p className="text-gray-600">
                    Find and extract information about company executives using LinkedIn and search engines.
                  </p>
                </div>
              </div>

              <div className="card">
                <div className="text-center">
                  <div className="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 mb-4">
                    <svg className="h-8 w-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold mb-2">Companies House Integration</h3>
                  <p className="text-gray-600">
                    Extract official company information from the UK Companies House registry.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Demo Section */}
        <div className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                See It In Action
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Submit your list of domains and get comprehensive company information in minutes.
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg shadow-lg p-6">
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th className="px-6 py-3">Domain</th>
                      <th className="px-6 py-3">Company Name</th>
                      <th className="px-6 py-3">Address</th>
                      <th className="px-6 py-3">Executive</th>
                      <th className="px-6 py-3">Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="px-6 py-4">example.com</td>
                      <td className="px-6 py-4">Example Limited</td>
                      <td className="px-6 py-4">123 Main Street, London, SW1A 1AA</td>
                      <td className="px-6 py-4">John Smith</td>
                      <td className="px-6 py-4">Companies House</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4">acme.co.uk</td>
                      <td className="px-6 py-4">Acme Corporation</td>
                      <td className="px-6 py-4">456 High Street, Manchester, M1 1AA</td>
                      <td className="px-6 py-4">Jane Doe</td>
                      <td className="px-6 py-4">LinkedIn</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4">techstartup.io</td>
                      <td className="px-6 py-4">TechStartup Limited</td>
                      <td className="px-6 py-4">789 Silicon Valley, San Francisco, CA 94107</td>
                      <td className="px-6 py-4">Mike Johnson</td>
                      <td className="px-6 py-4">Company Website</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-primary-600 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-3xl mx-auto">
              Join thousands of users who are already using BeScraped to automate their company data collection.
            </p>
            <a
              href="/dashboard"
              className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-primary-600 bg-white hover:bg-gray-100 md:text-lg md:px-10 transition-colors duration-200"
            >
              Start Using BeScraped
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Home;
