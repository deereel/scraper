# BeScraped - Company Information Extractor

## About BeScraped

BeScraped is an intelligent web scraping tool that automates the process of collecting company information from multiple public sources. It extracts valuable data such as company names, addresses, and executive details from websites, LinkedIn profiles, and official registries like the UK Companies House.

## Features

### 🎯 **Key Features**
- **Multiple Input Methods**: Manual entry, CSV/Excel upload, or Google Sheet import
- **Smart Scraping**: Analyzes company websites to find relevant pages (about, contact, team)
- **Multi-Source Extraction**: Combines data from:
  - Company websites
  - Google search results
  - LinkedIn profiles
  - UK Companies House registry
- **Data Quality**: Advanced scoring system ranks sources by reliability
- **Efficiency**: Async scraping with concurrent job processing
- **Export Options**: Download results as CSV or Excel

### 🚀 **Technical Features**
- **Frontend**: Next.js + React with Tailwind CSS
- **Backend**: FastAPI (Python)
- **Scraping**: Playwright + BeautifulSoup
- **Search**: Serper API for Google search integration
- **Database**: SQLite with PostgreSQL compatibility
- **Queue System**: Async background jobs

## Project Structure

```
scraper/
├── frontend/             # Next.js + React application
│   ├── components/       # Reusable UI components
│   ├── pages/            # Page components
│   ├── styles/           # Global styles
│   ├── package.json      # Frontend dependencies
│   ├── tsconfig.json     # TypeScript configuration
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── postcss.config.js  # PostCSS configuration
├── backend/              # FastAPI backend
│   ├── api/              # API routes
│   ├── scrapers/         # Scraping modules
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions
│   ├── models/           # Database models
│   ├── jobs/             # Background job processing
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Python dependencies
├── database/             # SQLite database file
└── README.md             # Project documentation
```

## Installation

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- pip (Python package manager)
- Playwright browser engines

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
playwright install
uvicorn main:app --reload
```

### Environment Variables

Create a `.env` file in the backend directory with:
```
SERPER_API_KEY=your_serper_api_key
GOOGLE_SHEETS_CREDENTIALS=credentials.json
```

## Usage

1. **Start the application**: 
   - Frontend runs on http://localhost:3000
   - Backend runs on http://localhost:8000

2. **Access the dashboard**: Navigate to http://localhost:3000/dashboard

3. **Submit domains**: 
   - Enter domain names manually (one per line)
   - Upload a CSV or Excel file
   - Enter a Google Sheet URL

4. **Start scraping**: Click "Start Scraping" to begin the process

5. **View results**: Results will be displayed in a table with source information

6. **Export data**: Download results as CSV or Excel

## Technologies Used

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API calls

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- Playwright
- BeautifulSoup4
- requests
- pandas

### Services
- Serper API for Google search
- Google Sheets API for sheet import
- LinkedIn scraping via search engines

## Architecture

### Data Flow
1. Input validation and domain normalization
2. Job queue management
3. Concurrent scraping with Playwright
4. Data extraction from multiple sources
5. Confidence scoring and merging
6. Database storage
7. Results display and export

### Source Reliability
- **Companies House**: 95% reliability
- **LinkedIn**: 85% reliability  
- **Company Website**: 70% reliability
- **Google Snippet**: 60% reliability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for educational purposes and legitimate business use. Always comply with website terms of service and applicable laws when scraping data.
