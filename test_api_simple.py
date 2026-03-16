"""
Test script to verify BeScraped API functionality (simplified version for Windows)
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print("Health Check:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {str(e)}")
        return False

def test_domain_normalization():
    """Test domain normalization endpoint"""
    try:
        domains = ["example.com", "www.example.co.uk", "http://test.org"]
        response = requests.post(f"{BASE_URL}/api/domains/normalize", json=domains)
        
        print("\nDomain Normalization:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                print(f"{result['original']} -> {result['normalized']} (Valid: {result['valid']})")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Domain Normalization Failed: {str(e)}")
        return False

def test_domain_validation():
    """Test domain validation endpoint"""
    try:
        domains = ["example.com", "invalid-domain", "123"]
        response = requests.post(f"{BASE_URL}/api/domains/validate", json=domains)
        
        print("\nDomain Validation:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                print(f"{result['domain']} -> Valid: {result['valid']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Domain Validation Failed: {str(e)}")
        return False

def test_get_companies():
    """Test getting companies from database"""
    try:
        response = requests.get(f"{BASE_URL}/api/companies")
        
        print("\nGet Companies:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of companies: {len(data['companies'])}")
            for company in data['companies'][:3]:
                print(f"{company['domain']}: {company['company_name']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Get Companies Failed: {str(e)}")
        return False

def test_scrape_job():
    """Test creating a scraping job"""
    try:
        domains = ["example.com"]
        response = requests.post(f"{BASE_URL}/api/jobs/scrape", json=domains)
        
        print("\nCreate Scraping Job:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Job IDs: {data['job_ids']}")
            print(f"Valid Domains: {data['valid_domains']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Create Scraping Job Failed: {str(e)}")
        return False

def test_get_jobs():
    """Test getting jobs from the queue"""
    try:
        response = requests.get(f"{BASE_URL}/api/jobs")
        
        print("\nGet Jobs:")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of jobs: {len(data['jobs'])}")
            for job in data['jobs'][:3]:
                print(f"Job {job['id']}: {job['status']} (Progress: {job['progress']})")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Get Jobs Failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing BeScraped API")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Domain Normalization", test_domain_normalization),
        ("Domain Validation", test_domain_validation),
        ("Get Companies", test_get_companies),
        ("Create Scraping Job", test_scrape_job),
        ("Get Jobs", test_get_jobs)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"[OK] {test_name} PASSED")
            else:
                failed += 1
                print(f"[FAILED] {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"[FAILED] {test_name} FAILED: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"Total: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\nAll tests passed!")
    else:
        print(f"\n{failed} test(s) failed!")

if __name__ == "__main__":
    main()
