"""
BeScraped Backend API
Purpose: FastAPI server for BeScraped application
Author: BeScraped Team
"""

import os
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.models.database import init_db, get_db, Company, ScrapingJob
from backend.utils.domain_normalizer import normalize_domain, validate_domain
from backend.services.google_sheets_importer import GoogleSheetsImporter
from backend.services.google_search_service import GoogleSearchService
from backend.services.data_merger import DataMerger
from backend.services.confidence_scorer import ConfidenceScorer
from backend.jobs.scraping_queue import ScrapingQueue
from backend.scrapers.address_extractor import AddressExtractor
from backend.scrapers.company_name_detector import CompanyNameDetector
from backend.scrapers.executive_extractor import ExecutiveExtractor
from backend.scrapers.website_crawler import WebsiteCrawler
from backend.scrapers.companies_house_scraper import CompaniesHouseScraper
from backend.scrapers.linkedin_scraper import LinkedInExecutiveDiscovery

# Initialize the database
init_db()

# Create FastAPI application
app = FastAPI(
    title="BeScraped API",
    description="API for automatic company information extraction",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
scoring_service = ConfidenceScorer()
merging_service = DataMerger()
address_extractor = AddressExtractor()
company_name_detector = CompanyNameDetector()
executive_extractor = ExecutiveExtractor()
crawler = WebsiteCrawler()
google_search = GoogleSearchService()

# Initialize new scrapers
try:
    companies_house_scraper = CompaniesHouseScraper()
except Exception as e:
    print(f"Failed to initialize Companies House scraper: {e}")
    companies_house_scraper = None

try:
    linkedin_scraper = LinkedInExecutiveDiscovery()
except Exception as e:
    print(f"Failed to initialize LinkedIn scraper: {e}")
    linkedin_scraper = None

# Initialize scraping queue
scraping_queue = None


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global scraping_queue
    scraping_queue = ScrapingQueue(max_concurrency=2)  # Reduced to 2 workers to prevent DB connection issues
    await scraping_queue.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on shutdown."""
    global scraping_queue
    if scraping_queue:
        await scraping_queue.stop()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "BeScraped API is running"}


@app.post("/api/domains/normalize")
def normalize_domains(domains: List[str]):
    """
    Normalize a list of domains.

    Args:
        domains: List of domains to normalize

    Returns:
        List of normalized domains
    """
    normalized = []
    for domain in domains:
        normalized_domain = normalize_domain(domain)
        normalized.append({
            'original': domain,
            'normalized': normalized_domain,
            'valid': validate_domain(normalized_domain)
        })
    return {'results': normalized}


@app.post("/api/domains/validate")
def validate_domains(domains: List[str]):
    """
    Validate a list of domains.

    Args:
        domains: List of domains to validate

    Returns:
        List of validation results
    """
    results = []
    for domain in domains:
        normalized = normalize_domain(domain)
        results.append({
            'domain': domain,
            'valid': validate_domain(normalized)
        })
    return {'results': results}


@app.post("/api/jobs/scrape")
async def scrape_domains(domains: List[str]):
    """
    Submit domains for scraping.

    Args:
        domains: List of domains to scrape

    Returns:
        Job IDs for each domain
    """
    valid_domains = []
    for domain in domains:
        normalized = normalize_domain(domain)
        if validate_domain(normalized):
            valid_domains.append(normalized)

    if not valid_domains:
        raise HTTPException(status_code=400, detail="No valid domains provided")

    job_ids = []
    for domain in valid_domains:
        job_id = await scraping_queue.add_job(domain)
        job_ids.append(job_id)

    return {'job_ids': job_ids, 'valid_domains': valid_domains}


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: int):
    """
    Get job information by ID.

    Args:
        job_id: Job ID

    Returns:
        Job information
    """
    job_info = await scraping_queue.get_job(job_id)
    if not job_info:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_info


@app.get("/api/jobs")
async def get_jobs(status: Optional[str] = None):
    """
    Get list of scraping jobs.

    Args:
        status: Filter by job status (pending, running, completed, failed)

    Returns:
        List of jobs
    """
    if status == "pending":
        return {'jobs': await scraping_queue.get_pending_jobs()}
    elif status == "running":
        return {'jobs': await scraping_queue.get_running_jobs()}
    elif status == "completed":
        return {'jobs': await scraping_queue.get_completed_jobs()}
    else:
        db = next(get_db())
        jobs = db.query(ScrapingJob).all()
        return {
            'jobs': [
                {
                    'id': job.id,
                    'domain': job.domain,
                    'status': job.status,
                    'progress': job.progress,
                    'error_message': job.error_message,
                    'created_at': job.created_at.isoformat(),
                    'updated_at': job.updated_at.isoformat()
                }
                for job in jobs
            ]
        }


@app.get("/api/companies")
def get_companies(db: Session = Depends(get_db)):
    """
    Get all companies from database.

    Returns:
        List of companies
    """
    companies = db.query(Company).all()
    return {
        'companies': [
            {
                'id': company.id,
                'domain': company.domain,
                'company_name': company.company_name,
                'address': company.address,
                'executive_first_name': company.executive_first_name,
                'executive_last_name': company.executive_last_name,
                'source': company.source,
                'confidence': company.confidence,
                'created_at': company.created_at.isoformat(),
                'updated_at': company.updated_at.isoformat()
            }
            for company in companies
        ]
    }


@app.get("/api/companies/{domain}")
def get_company(domain: str, db: Session = Depends(get_db)):
    """
    Get company information by domain.

    Args:
        domain: Domain name

    Returns:
        Company information
    """
    normalized_domain = normalize_domain(domain)
    company = db.query(Company).filter(Company.domain == normalized_domain).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company.to_dict()


@app.post("/api/companies")
async def scrape_company(domain: str, db: Session = Depends(get_db)):
    """
    Scrape company information from a single domain.

    Args:
        domain: Domain to scrape

    Returns:
        Scraping job information
    """
    normalized_domain = normalize_domain(domain)
    if not validate_domain(normalized_domain):
        raise HTTPException(status_code=400, detail="Invalid domain")

    # Check if company already exists
    existing_company = db.query(Company).filter(Company.domain == normalized_domain).first()
    if existing_company:
        return existing_company.to_dict()

    # Add to scraping queue
    job_id = await scraping_queue.add_job(normalized_domain)
    job_info = await scraping_queue.get_job(job_id)

    return job_info


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
