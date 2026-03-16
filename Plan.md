MASTER PROJECT PROMPT

Use this once before generating any code so all agents follow the same architecture.

You are building a production-ready web application called "BeScraped".

Purpose:
BeScraped automatically collects company information from public sources when given company website domains.

Inputs supported:
• Manual entry of multiple domains
• CSV or Excel file upload
• Google Sheet containing domains

Sources to search and scrape:
1. Company website
2. Google search results
3. LinkedIn
4. UK Companies House registry
5. Website pages such as /about /contact /team

Data to extract:
• Company full name
• Company address
• Highest ranking official's first name
• Highest ranking official's last name
• Source of information

Output:
Display results in a dashboard table and allow export to CSV or Excel.

Architecture requirements:

Frontend:
Next.js + React
Tailwind CSS or Bootstrap UI

Backend:
Python FastAPI server

Scraping Engine:
Playwright + BeautifulSoup

Search Integration:
Serper API or SerpAPI for Google search

Database:
SQLite initially but designed for PostgreSQL compatibility

Queue System:
Async background jobs for scraping domains

Important rules:
• Scraping must be asynchronous
• Handle errors and timeouts gracefully
• Avoid scraping the same domain twice
• Clean and normalize domains before scraping
• Merge results from multiple sources with reliability scoring
SECTION 1 — PROJECT STRUCTURE

Prompt:

Create the full folder structure for a web application called BeScraped.

Use this stack:

Frontend:
Next.js + React
Tailwind CSS

Backend:
Python FastAPI

Scraping:
Playwright + BeautifulSoup

Database:
SQLite

Structure:

/frontend
/components
/pages
/styles

/backend
/api
/scrapers
/services
/utils
/models
/jobs

/database

Ensure backend and frontend can communicate through REST APIs.
SECTION 2 — LANDING PAGE

Prompt:

Create the landing page for BeScraped.

Page layout:

Header
Logo: BeScraped
Navigation: Home, Dashboard, Docs

Hero Section
Headline:
"Instant Company Data Extraction"

Subheadline:
"Extract company names, addresses and executives from websites, LinkedIn and official registries automatically."

Button:
"Start Scraping"

Features Section (3 cards)
• Website Scraping
• Executive Discovery
• Companies House Integration

Demo Table Section
Show example results table.

Footer
Privacy
Terms
Documentation

Design requirements:
Responsive
Modern SaaS design
Tailwind CSS styling
SECTION 3 — DASHBOARD UI

Prompt:

Create the main BeScraped dashboard page.

The dashboard should allow users to submit domains for scraping.

Input options:

1. Textarea where users paste multiple domains (one per line)
2. Upload CSV or Excel file
3. Input Google Sheet URL

Controls:
Start Scraping button
Clear Inputs button

Results section:
Table with columns:

Domain
Company Name
Company Address
Executive First Name
Executive Last Name
Source

Add loading indicators while scraping jobs are running.
SECTION 4 — DOMAIN NORMALIZATION

Prompt:

Create a backend utility function that normalizes company domains.

Input examples:
http://example.com
https://example.com/
www.example.com

Output:
example.com

Rules:
Remove protocol
Remove www prefix
Remove trailing slash
Trim whitespace

Return normalized domain.
SECTION 5 — GOOGLE SHEET IMPORTER

Prompt:

Create a backend service that imports domains from a Google Sheet.

Input:
Google Sheet URL

Steps:
Extract sheet ID
Use Google Sheets API to read rows
Extract domains from first column

Return data as:

[
 { "domain": "example.com" }
]

Remove duplicates.
SECTION 6 — DOMAIN DISCOVERY ENGINE

Prompt:

Create a discovery engine that finds relevant pages for a company domain.

For each domain run search queries such as:

site:DOMAIN about
site:DOMAIN contact
site:DOMAIN team
site:DOMAIN leadership
site:linkedin.com DOMAIN CEO
DOMAIN site:find-and-update.company-information.service.gov.uk

Return discovered URLs categorized by source.
SECTION 7 — GOOGLE SEARCH SERVICE

Prompt:

Create a Google search service using Serper API.

Input:
domain

Run queries:

site:DOMAIN CEO
site:DOMAIN founder
site:DOMAIN managing director
site:linkedin.com DOMAIN CEO
DOMAIN site:find-and-update.company-information.service.gov.uk

Return top search results.
SECTION 8 — SMART WEBSITE CRAWLER

Prompt:

Create a website crawler using Playwright.

Process:

1. Load homepage
2. Extract internal links
3. Identify important pages such as:

about
contact
team
leadership

Crawl these pages.

Return page HTML content.
SECTION 9 — HTML TEXT CLEANER

Prompt:

Create a module that converts HTML to clean text.

Remove:

script tags
style tags
navigation elements
duplicate whitespace

Return plain text content.
SECTION 10 — COMPANY ADDRESS EXTRACTOR

Prompt:

Create a function that extracts UK company addresses.

Detection methods:

UK postcode regex
Street keywords:

street
road
lane
avenue
drive
court
way

Return the most complete address block found.
SECTION 11 — COMPANY NAME DETECTOR

Prompt:

Create a module that detects the company name.

Use these sources:

HTML title tag
meta og:site_name
Companies House results

Return most confident company name.
SECTION 12 — EXECUTIVE NAME EXTRACTION

Prompt:

Create an extractor that finds the highest ranking executive.

Search for titles:

CEO
Founder
Managing Director
Owner
President
Director

Extract:

first name
last name
title
SECTION 13 — LINKEDIN EXECUTIVE DISCOVERY

Prompt:

Create a service that finds LinkedIn profiles for company executives.

Search query:

site:linkedin.com DOMAIN CEO

Extract:

first name
last name
title
LinkedIn URL
SECTION 14 — COMPANIES HOUSE SCRAPER

Prompt:

Create a scraper for the UK Companies House registry.

Website:
https://find-and-update.company-information.service.gov.uk

Input:
company name or domain

Extract:

company name
registered office address
director names

Return structured data.
SECTION 15 — DATA CONFIDENCE SCORING

Prompt:

Create a scoring engine that ranks sources by reliability.

Score values:

Companies House = 95
LinkedIn = 85
Company Website = 70
Google Snippet = 60

Use highest scoring data when merging results.
SECTION 16 — DATA MERGING ENGINE

Prompt:

Create a data merging engine.

Combine results from:

website scraper
google search
linkedin
companies house

Return final structured record:

domain
company_name
address
executive_first_name
executive_last_name
source
SECTION 17 — DATABASE SCHEMA

Prompt:

Create database schema for scraped company records.

Table: companies

Fields:

id
domain
company_name
address
executive_first_name
executive_last_name
source
created_at
SECTION 18 — SCRAPING JOB QUEUE

Prompt:

Create an asynchronous scraping queue.

Process:

User submits domains
Domains added to job queue
Workers scrape domains
Results stored in database

Limit concurrency to 5 domains at once.
SECTION 19 — RESULTS TABLE UI

Prompt:

Create a React component displaying results in a table.

Columns:

Domain
Company Name
Address
Executive First Name
Executive Last Name
Source

Features:

Pagination
Sorting
Filtering
SECTION 20 — EXPORT TO SPREADSHEET

Prompt:

Create export functionality.

Allow download as:

CSV
Excel

File name:
bescraped_results.xlsx
SECTION 21 — ERROR HANDLING

Prompt:

Add error handling for:

404 websites
blocked scraping requests
invalid domains
rate limits

Log failures but continue processing other domains.
SECTION 22 — PERFORMANCE OPTIMIZATION

Prompt:

Optimize scraping system.

Requirements:

Process multiple domains in parallel
Limit concurrency to prevent blocking
Retry failed requests
Cache previously scraped domains
FINAL RESULT

BeScraped will:

Accept domains or Google Sheets

Discover relevant sources

Scrape websites, LinkedIn and Companies House

Extract company name, address and executive

Display results in dashboard

Export results to spreadsheet