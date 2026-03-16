import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';

interface Company {
  id: number;
  domain: string;
  company_name: string | null;
  address: string | null;
  executive_first_name: string | null;
  executive_last_name: string | null;
  source: string | null;
  confidence: number | null;
  created_at: string;
  updated_at: string;
}

interface Job {
  id: number;
  domain: string;
  status: string;
  progress: number;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

const Dashboard: React.FC = () => {
  const [domains, setDomains] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [googleSheetUrl, setGoogleSheetUrl] = useState<string>('');
  const [isScraping, setIsScraping] = useState<boolean>(false);
  const [scrapingProgress, setScrapingProgress] = useState<number>(0);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);

  const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDomains(e.target.value);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleGoogleSheetUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setGoogleSheetUrl(e.target.value);
  };

  const handleClearInputs = () => {
    setDomains('');
    setFile(null);
    setGoogleSheetUrl('');
  };

  // Fetch companies from backend
  const fetchCompanies = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/companies');
      if (response.ok) {
        const data = await response.json();
        setCompanies(data.companies || []);
      }
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  // Fetch jobs from backend
  const fetchJobs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/jobs');
      if (response.ok) {
        const data = await response.json();
        setJobs(data.jobs || []);
        // Update scraping progress
        if (data.length > 0) {
          const activeJob = data.find((job: Job) => job.status === 'running');
          if (activeJob) {
            setScrapingProgress(activeJob.progress);
          } else if (data.every((job: Job) => job.status === 'completed')) {
            setIsScraping(false);
            setScrapingProgress(100);
            // Refresh companies after scraping completes
            fetchCompanies();
          }
        }
      }
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchCompanies();
    fetchJobs();
  }, []);

  // Poll jobs while scraping
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isScraping) {
      interval = setInterval(() => {
        fetchJobs();
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isScraping]);

  const handleStartScraping = async () => {
    setIsScraping(true);
    setScrapingProgress(0);

    // Prepare data for scraping
    const data = new FormData();
    
    if (domains) {
      data.append('domains', domains);
    }
    
    if (file) {
      data.append('file', file);
    }
    
    if (googleSheetUrl) {
      data.append('google_sheet_url', googleSheetUrl);
    }

    try {
      // Prepare domains array from inputs
      const domainsArray: string[] = [];
      
      if (domains) {
        domainsArray.push(...domains.split('\n').filter(domain => domain.trim()));
      }
      
      const response = await fetch('http://localhost:8000/api/jobs/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(domainsArray),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Scraping started:', result);
      } else {
        console.error('Error starting scraping:', response.statusText);
        setIsScraping(false);
      }
    } catch (error) {
      console.error('Error starting scraping:', error);
      setIsScraping(false);
    }
  };

  return (
    <Layout>
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

          {/* Input Options */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Manual Input */}
            <div className="lg:col-span-2">
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">Manual Domain Input</h2>
                <div className="mb-4">
                  <textarea
                    value={domains}
                    onChange={handleTextAreaChange}
                    placeholder="Enter domain names one per line (e.g., example.com&#10;acme.co.uk&#10;techstartup.io)"
                    className="input-field"
                    rows={6}
                    disabled={isScraping}
                  />
                </div>
              </div>
            </div>

            {/* File Upload */}
            <div className="lg:col-span-1">
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">File Upload</h2>
                <div className="mb-4">
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileChange}
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-primary-50 file:text-primary-600 hover:file:bg-primary-100"
                    disabled={isScraping}
                  />
                  {file && (
                    <div className="mt-2 text-sm text-gray-600">
                      Selected file: <span className="font-medium">{file.name}</span>
                    </div>
                  )}
                </div>

                {/* Google Sheet URL */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Google Sheet URL
                  </label>
                  <input
                    type="url"
                    value={googleSheetUrl}
                    onChange={handleGoogleSheetUrlChange}
                    placeholder="https://docs.google.com/spreadsheets/d/..."
                    className="input-field"
                    disabled={isScraping}
                  />
                </div>

                {/* Controls */}
                <div className="flex flex-col space-y-3">
                  <button
                    onClick={handleStartScraping}
                    disabled={isScraping || (!domains && !file && !googleSheetUrl)}
                    className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isScraping ? 'Scraping...' : 'Start Scraping'}
                  </button>
                  <button
                    onClick={handleClearInputs}
                    disabled={isScraping}
                    className="btn-secondary"
                  >
                    Clear Inputs
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          {isScraping && (
            <div className="mb-8">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-medium mb-4">Scraping Progress</h3>
                <div className="mb-2">
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Domains processed</span>
                    <span>{scrapingProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-primary-600 h-2.5 rounded-full transition-all duration-300"
                      style={{ width: `${scrapingProgress}%` }}
                    ></div>
                  </div>
                </div>
                <p className="text-sm text-gray-500 mt-2">
                  Estimated time remaining: {Math.max(0, 50 - (scrapingProgress / 2))} seconds
                </p>
              </div>
            </div>
          )}

          {/* Results Table */}
          <div className="mb-8">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Results</h2>
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th className="px-6 py-3">Domain</th>
                      <th className="px-6 py-3">Company Name</th>
                      <th className="px-6 py-3">Address</th>
                      <th className="px-6 py-3">Executive</th>
                      <th className="px-6 py-3">Source</th>
                      <th className="px-6 py-3">Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {companies.length > 0 ? (
                      companies.map((company: Company) => (
                        <tr key={company.id}>
                          <td className="px-6 py-4">{company.domain}</td>
                          <td className="px-6 py-4">{company.company_name || '-'}</td>
                          <td className="px-6 py-4">{company.address || '-'}</td>
                          <td className="px-6 py-4">
                            {company.executive_first_name && company.executive_last_name 
                              ? `${company.executive_first_name} ${company.executive_last_name}` 
                              : '-'
                            }
                          </td>
                          <td className="px-6 py-4">{company.source || '-'}</td>
                          <td className="px-6 py-4">
                            {company.confidence !== null ? `${company.confidence}%` : '-'}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                          No companies found. Start scraping to see results.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              {/* Export Button */}
              <div className="mt-4 flex justify-end">
                <button 
                  className="btn-primary"
                  disabled={companies.length === 0}
                  onClick={async () => {
                    try {
                      const response = await fetch('http://localhost:8000/api/export');
                      if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'companies.csv';
                        a.click();
                        window.URL.revokeObjectURL(url);
                      }
                    } catch (error) {
                      console.error('Error exporting CSV:', error);
                    }
                  }}
                >
                  Export to CSV
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
