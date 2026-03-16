const axios = require('axios');

async function testOptimizeCoUk() {
  console.log('Testing optimize.co.uk...');
  
  try {
    // Test scraping optimize.co.uk
    console.log('\n1. Testing scraping optimize.co.uk...');
    const response = await axios.post('http://localhost:8000/api/jobs/scrape', 
      ['optimize.co.uk'],
      { 
        headers: { 
          'Content-Type': 'application/json'
        }
      }
    );
    console.log('Scraping request:', response.status === 200 ? '✅ OK' : '❌ Failed');
    if (response.status === 200) {
      console.log('Response:', response.data);
    }
    
    // Check jobs status
    console.log('\n2. Checking jobs status...');
    const jobsResponse = await axios.get('http://localhost:8000/api/jobs');
    console.log('Jobs status:', jobsResponse.status === 200 ? '✅ OK' : '❌ Failed');
    console.log('Number of jobs:', jobsResponse.data.jobs.length);
    jobsResponse.data.jobs.forEach(job => {
      console.log(`Job ${job.id}: ${job.domain} - ${job.status} - ${job.progress}%`);
    });
    
    // Wait for scraping to complete
    console.log('\n3. Waiting for scraping to complete...');
    let completed = false;
    for (let i = 0; i < 60; i++) {
      const jobsCheck = await axios.get('http://localhost:8000/api/jobs');
      const optimizeJob = jobsCheck.data.jobs.find(job => job.domain === 'optimize.co.uk');
      
      if (optimizeJob) {
        console.log(`Job status: ${optimizeJob.status} (${optimizeJob.progress}%)`);
        
        if (optimizeJob.status === 'completed') {
          completed = true;
          break;
        } else if (optimizeJob.status === 'failed') {
          console.log('Job failed:', optimizeJob.error_message);
          break;
        }
      }
      
      await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
    }
    
    if (completed) {
      // Check if company was added
      console.log('\n4. Checking company data...');
      const companiesResponse = await axios.get('http://localhost:8000/api/companies');
      const optimizeCompany = companiesResponse.data.companies.find(company => company.domain === 'optimize.co.uk');
      
      if (optimizeCompany) {
        console.log('✅ Company found:');
        console.log('Domain:', optimizeCompany.domain);
        console.log('Company Name:', optimizeCompany.company_name);
        console.log('Address:', optimizeCompany.address);
        console.log('Executive:', optimizeCompany.executive_first_name, optimizeCompany.executive_last_name);
        console.log('Source:', optimizeCompany.source);
        console.log('Confidence:', optimizeCompany.confidence);
      } else {
        console.log('❌ Company not found');
      }
    }
    
  } catch (error) {
    console.error('\n❌ Error:', error.response ? error.response.data : error.message);
  }
}

testOptimizeCoUk();
