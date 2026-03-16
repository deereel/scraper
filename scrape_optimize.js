const axios = require('axios');

async function scrapeOptimize() {
  try {
    const response = await axios.post('http://localhost:8000/api/jobs/scrape', ['optimize.co.uk'], {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    console.log('Scraping job created successfully:', response.data);
  } catch (error) {
    console.error('Error creating scraping job:', error.response?.data || error.message);
  }
}

scrapeOptimize();
