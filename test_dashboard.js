const axios = require('axios');

async function testDashboard() {
  console.log('Testing BeScraped Dashboard API...');
  
  try {
    // Test 1: Check if backend is running
    console.log('\n1. Checking backend health...');
    const healthResponse = await axios.get('http://localhost:8000/');
    console.log('Health check:', healthResponse.status === 200 ? '✅ OK' : '❌ Failed');
    if (healthResponse.status === 200) {
      console.log('Response:', healthResponse.data);
    }
    
    // Test 2: Check if companies API endpoint is working
    console.log('\n2. Checking companies API...');
    const companiesResponse = await axios.get('http://localhost:8000/api/companies');
    console.log('Companies API:', companiesResponse.status === 200 ? '✅ OK' : '❌ Failed');
    console.log('Number of companies:', companiesResponse.data.companies.length);
    
    // Test 3: Check if jobs API endpoint is working
    console.log('\n3. Checking jobs API...');
    const jobsResponse = await axios.get('http://localhost:8000/api/jobs');
    console.log('Jobs API:', jobsResponse.status === 200 ? '✅ OK' : '❌ Failed');
    console.log('Number of jobs:', jobsResponse.data.jobs.length);
    
    // Test 4: Test scraping with sample domains
    console.log('\n4. Testing scraping functionality...');
    const testDomains = ['example.com', 'acme.co.uk', 'techstartup.io'];
    const scrapeResponse = await axios.post('http://localhost:8000/api/jobs/scrape', 
      testDomains,
      { 
        headers: { 
          'Content-Type': 'application/json'
        }
      }
    );
    console.log('Scraping request:', scrapeResponse.status === 200 ? '✅ OK' : '❌ Failed');
    if (scrapeResponse.status === 200) {
      console.log('Response:', scrapeResponse.data);
    }
    
    console.log('\n✅ All tests completed successfully!');
    
  } catch (error) {
    console.error('\n❌ Error:', error.response ? error.response.data : error.message);
  }
}

testDashboard();
