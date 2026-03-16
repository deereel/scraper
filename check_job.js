const axios = require('axios');

async function checkJobStatus(jobId) {
  try {
    const response = await axios.get(`http://localhost:8000/api/jobs/${jobId}`);
    console.log('Job status:', response.data);
  } catch (error) {
    console.error('Error checking job status:', error.response?.data || error.message);
  }
}

async function getAllJobs() {
  try {
    const response = await axios.get('http://localhost:8000/api/jobs');
    console.log('All jobs:', response.data);
  } catch (error) {
    console.error('Error getting jobs:', error.response?.data || error.message);
  }
}

async function checkCompanies() {
  try {
    const response = await axios.get('http://localhost:8000/api/companies');
    console.log('Companies:', response.data);
  } catch (error) {
    console.error('Error getting companies:', error.response?.data || error.message);
  }
}

// Check job 5 (the one we just created)
checkJobStatus(5);

// Wait a few seconds and check again
setTimeout(async () => {
  console.log('\n--- After 5 seconds ---');
  await checkJobStatus(5);
  await getAllJobs();
  await checkCompanies();
}, 5000);

// Wait a bit longer and check one more time
setTimeout(async () => {
  console.log('\n--- After 15 seconds ---');
  await checkJobStatus(5);
  await getAllJobs();
  await checkCompanies();
}, 15000);
