"""
Scraping Job Queue for BeScraped
Purpose: Manage asynchronous scraping jobs
Author: BeScraped Team
"""

import asyncio
import time
from typing import List, Dict, Optional
import concurrent.futures
from backend.models.database import ScrapingJob, get_db, Company
from backend.services.confidence_scorer import ConfidenceScorer
from backend.services.data_merger import DataMerger
from backend.scrapers.address_extractor import AddressExtractor
from backend.scrapers.company_name_detector import CompanyNameDetector
from backend.scrapers.executive_extractor import ExecutiveExtractor
from backend.scrapers.website_crawler import WebsiteCrawler
from backend.scrapers.companies_house_scraper import CompaniesHouseScraper
from backend.scrapers.linkedin_scraper import LinkedInExecutiveDiscovery
from backend.services.google_search_service import GoogleSearchService


class ScrapingQueue:
    """Queue for managing scraping jobs with concurrency control."""

    def __init__(self, max_concurrency: int = 5):
        """
        Initialize scraping queue.

        Args:
            max_concurrency: Maximum number of concurrent scraping jobs
        """
        self.queue = asyncio.Queue()
        self.max_concurrency = max_concurrency
        self.running = False
        self.workers = []
        self.scorer = ConfidenceScorer()
        self.merger = DataMerger()
        
        # Initialize scrapers
        self.address_extractor = AddressExtractor()
        self.company_name_detector = CompanyNameDetector()
        self.executive_extractor = ExecutiveExtractor()
        self.crawler = WebsiteCrawler()
        self.google_search = GoogleSearchService()
        
        # Initialize optional scrapers (may fail if API keys are missing)
        try:
            self.companies_house_scraper = CompaniesHouseScraper()
        except Exception as e:
            print(f"Failed to initialize Companies House scraper: {e}")
            self.companies_house_scraper = None
            
        try:
            self.linkedin_scraper = LinkedInExecutiveDiscovery()
        except Exception as e:
            print(f"Failed to initialize LinkedIn scraper: {e}")
            self.linkedin_scraper = None

    async def add_job(self, domain: str) -> int:
        """
        Add a domain to the scraping queue.

        Args:
            domain: Domain to scrape

        Returns:
            Job ID
        """
        # Check if job already exists
        db = next(get_db())
        existing_job = db.query(ScrapingJob).filter(
            ScrapingJob.domain == domain,
            ScrapingJob.status.in_(["pending", "running"])
        ).first()

        if existing_job:
            return existing_job.id

        # Create new job
        new_job = ScrapingJob(
            domain=domain,
            status="pending",
            progress=0
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        await self.queue.put(new_job.id)
        return new_job.id

    async def get_job(self, job_id: int) -> Optional[Dict]:
        """
        Get job information by ID.

        Args:
            job_id: Job ID

        Returns:
            Job information
        """
        db = next(get_db())
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        if job:
            return {
                'id': job.id,
                'domain': job.domain,
                'status': job.status,
                'progress': job.progress,
                'error_message': job.error_message,
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            }
        return None

    async def update_job_status(self, job_id: int, status: str,
                               progress: int = None, error_message: str = None):
        """
        Update job status.

        Args:
            job_id: Job ID
            status: New status
            progress: Progress percentage
            error_message: Error message
        """
        db = next(get_db())
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if error_message:
                job.error_message = error_message
            db.commit()

    async def worker(self):
        """Worker to process scraping jobs from the queue."""
        while self.running:
            try:
                job_id = await asyncio.wait_for(self.queue.get(), timeout=1)
            except asyncio.TimeoutError:
                continue

            await self.process_job(job_id)
            self.queue.task_done()

    async def process_job(self, job_id: int):
        """
        Process a single scraping job.

        Args:
            job_id: Job ID
        """
        try:
            # Update job status to running
            await self.update_job_status(job_id, "running", progress=10)

            # Get job details
            db = next(get_db())
            job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
            if not job:
                return

            domain = str(job.domain)

            await self.update_job_status(job_id, "running", progress=30)
            
            # Step 1: Crawl website (using async method)
            try:
                crawled_data = await self.crawler.crawl(domain)
                # Extract HTML content from homepage
                html_content = ""
                base_url = f"https://{domain}"
                if base_url in crawled_data:
                    html_content = crawled_data[base_url]['content']
                else:
                    # Fallback to first available page content
                    for url in crawled_data:
                        if 'content' in crawled_data[url]:
                            html_content = crawled_data[url]['content']
                            break
            except Exception as e:
                raise Exception(f"Failed to crawl website: {str(e)}")

            await self.update_job_status(job_id, "running", progress=50)
            
            # Step 2: Clean and extract information
            from backend.utils.html_cleaner import HTMLTextCleaner
            cleaner = HTMLTextCleaner()
            cleaned_text = cleaner.clean_html(html_content)

            # Extract company name
            company_name = None
            try:
                company_name_result = self.company_name_detector.detect_company_name(html_content, cleaned_text)
                if company_name_result:
                    company_name = company_name_result.get('name', None)
            except Exception as e:
                print(f"Error extracting company name: {e}")

            # Extract address
            address = None
            try:
                addresses = self.address_extractor.extract_addresses(cleaned_text)
                if addresses:
                    address = addresses[0].get('address', None)
            except Exception as e:
                print(f"Error extracting address: {e}")

            # Extract executive information
            executive_first_name = None
            executive_last_name = None
            try:
                executives = self.executive_extractor.extract_executives(cleaned_text)
                if executives:
                    executive = executives[0]
                    executive_first_name = executive.get('first_name', None)
                    executive_last_name = executive.get('last_name', None)
            except Exception as e:
                print(f"Error extracting executive information: {e}")

            await self.update_job_status(job_id, "running", progress=80)
            
            # Step 3: Save to database
            existing = db.query(Company).filter(Company.domain == domain).first()
            if existing:
                # Update existing record
                existing.company_name = company_name
                existing.address = address
                existing.executive_first_name = executive_first_name
                existing.executive_last_name = executive_last_name
                existing.confidence = self.scorer.get_source_score('website')
                existing.source = 'website'
            else:
                # Create new record
                new_company = Company(
                    domain=domain,
                    company_name=company_name,
                    address=address,
                    executive_first_name=executive_first_name,
                    executive_last_name=executive_last_name,
                    confidence=self.scorer.get_source_score('website'),
                    source='website'
                )
                db.add(new_company)

            db.commit()

            # Complete the job
            await self.update_job_status(job_id, "completed", progress=100)
            print(f"Job {job_id} completed successfully")

        except Exception as e:
            await self.update_job_status(
                job_id, "failed",
                error_message=str(e)
            )
            print(f"Job {job_id} failed: {str(e)}")

    async def start(self):
        """Start the scraping queue workers."""
        if self.running:
            return

        self.running = True
        for _ in range(self.max_concurrency):
            worker_task = asyncio.create_task(self.worker())
            self.workers.append(worker_task)
        print(f"Scraping queue started with {self.max_concurrency} workers")

    async def stop(self):
        """Stop the scraping queue workers."""
        self.running = False
        for worker_task in self.workers:
            worker_task.cancel()
        try:
            await asyncio.gather(*self.workers, return_exceptions=True)
        except Exception:
            pass
        self.workers.clear()
        print("Scraping queue stopped")

    async def get_queue_size(self) -> int:
        """Get current queue size."""
        return self.queue.qsize()

    async def get_pending_jobs(self) -> List[Dict]:
        """Get list of pending jobs."""
        db = next(get_db())
        jobs = db.query(ScrapingJob).filter(ScrapingJob.status == "pending").all()
        return [
            {
                'id': job.id,
                'domain': job.domain,
                'created_at': job.created_at.isoformat()
            }
            for job in jobs
        ]

    async def get_running_jobs(self) -> List[Dict]:
        """Get list of running jobs."""
        db = next(get_db())
        jobs = db.query(ScrapingJob).filter(ScrapingJob.status == "running").all()
        return [
            {
                'id': job.id,
                'domain': job.domain,
                'progress': job.progress,
                'created_at': job.created_at.isoformat()
            }
            for job in jobs
        ]

    async def get_completed_jobs(self) -> List[Dict]:
        """Get list of completed jobs."""
        db = next(get_db())
        jobs = db.query(ScrapingJob).filter(ScrapingJob.status == "completed").all()
        return [
            {
                'id': job.id,
                'domain': job.domain,
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            }
            for job in jobs
        ]


async def main():
    """Test function."""
    queue = ScrapingQueue(max_concurrency=2)
    await queue.start()

    # Add some test jobs
    print("Adding test jobs...")
    job_ids = []
    test_domains = ["example.com", "google.com", "github.com", "stackoverflow.com"]
    for domain in test_domains:
        job_id = await queue.add_job(domain)
        job_ids.append(job_id)
        print(f"Added job {job_id} for domain {domain}")

    # Check queue status
    print(f"\nQueue size: {await queue.get_queue_size()}")
    print(f"Pending jobs: {await queue.get_pending_jobs()}")

    # Wait for jobs to complete
    await asyncio.sleep(1)
    print(f"\nRunning jobs: {await queue.get_running_jobs()}")

    await asyncio.sleep(12)

    # Check final status
    print(f"\nQueue size: {await queue.get_queue_size()}")
    print(f"Completed jobs: {await queue.get_completed_jobs()}")

    # Stop the queue
    await queue.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
