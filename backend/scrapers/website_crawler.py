"""
Website Crawler for BeScraped
Purpose: Crawl company websites and extract HTML content
Author: BeScraped Team
"""

import asyncio
import re
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Page


class WebsiteCrawler:
    """Crawl company websites and extract HTML content."""

    def __init__(self):
        """Initialize website crawler."""
        self.important_pages = [
            'about', 'contact', 'team', 'leadership', 'management',
            'careers', 'who-we-are', 'our-team', 'executive-team',
            'board-of-directors', 'company', 'about-us', 'contact-us'
        ]

        self.visited_urls = set()
        self.crawled_data = {}

    async def crawl(self, domain: str, max_pages: int = 10) -> Dict:
        """
        Crawl a website and extract content from important pages.

        Args:
            domain: Domain to crawl
            max_pages: Maximum number of pages to crawl

        Returns:
            Dictionary containing crawled pages and their content
        """
        # Reset state for each crawl
        self.visited_urls.clear()
        self.crawled_data.clear()

        base_url = f"https://{domain}"

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Crawl homepage first
                await self._crawl_page(page, base_url)

                # Find and crawl important pages
                for page_type in self.important_pages:
                    if len(self.visited_urls) >= max_pages:
                        break

                    # Look for URLs containing important page patterns
                    await self._find_and_crawl_pages(page, base_url, page_type)

                await browser.close()

            return self.crawled_data

        except Exception as e:
            print(f"Error crawling {domain}: {str(e)}")
            self.crawled_data['error'] = str(e)
            return self.crawled_data

    async def _crawl_page(self, page: Page, url: str) -> None:
        """
        Crawl a single page and extract content.

        Args:
            page: Playwright page object
            url: URL to crawl
        """
        if url in self.visited_urls:
            return

        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
            html_content = await page.content()

            self.visited_urls.add(url)
            self.crawled_data[url] = {
                'content': html_content,
                'title': await page.title()
            }

            print(f"Successfully crawled: {url}")

        except Exception as e:
            print(f"Failed to crawl {url}: {str(e)}")

    async def _find_and_crawl_pages(self, page: Page, base_url: str, page_type: str) -> None:
        """
        Find and crawl pages matching a specific type.

        Args:
            page: Playwright page object
            base_url: Base URL of the website
            page_type: Page type to look for
        """
        try:
            # Go to homepage first to find internal links
            await page.goto(base_url, wait_until='networkidle', timeout=30000)

            # Get all internal links from the page
            links = await page.evaluate('''() => {
                const links = [];
                document.querySelectorAll('a').forEach(a => {
                    const href = a.getAttribute('href');
                    if (href && !href.startsWith('http') && !href.startsWith('javascript')) {
                        links.push(href);
                    }
                });
                return links;
            }''')

            # Filter links matching the page type
            pattern = re.compile(rf'.*{page_type}.*', re.IGNORECASE)
            filtered_links = [
                urljoin(base_url, link.strip())
                for link in links
                if pattern.search(link)
            ]

            # Crawl unique links
            for link in filtered_links:
                if link not in self.visited_urls:
                    await self._crawl_page(page, link)
                    if len(self.visited_urls) >= 10:
                        break

        except Exception as e:
            print(f"Error finding {page_type} pages: {str(e)}")

    def extract_relevant_links(self, html_content: str, base_url: str) -> List[str]:
        """
        Extract relevant links from HTML content.

        Args:
            html_content: HTML content to parse
            base_url: Base URL for relative links

        Returns:
            List of relevant internal links
        """
        relevant_links = []
        pattern = re.compile(r'href=["\']?([^"\'\s>]*)["\'\s>]')

        for match in pattern.finditer(html_content):
            href = match.group(1)
            if href and not href.startswith('http') and not href.startswith('javascript'):
                full_url = urljoin(base_url, href.strip())
                parsed_url = urlparse(full_url)

                # Only include links to the same domain
                if parsed_url.netloc == urlparse(base_url).netloc:
                    for page_type in self.important_pages:
                        if page_type in parsed_url.path.lower():
                            relevant_links.append(full_url)
                            break

        return list(set(relevant_links))

    def get_crawled_data(self) -> Dict:
        """
        Get the crawled data.

        Returns:
            Crawled data dictionary
        """
        return self.crawled_data


async def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python website_crawler.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    crawler = WebsiteCrawler()

    print(f"Crawling {domain}...")
    data = await crawler.crawl(domain)

    print(f"\nCrawl complete. Found {len(data)} pages:")
    for url, info in data.items():
        print(f"- {url} ({info['title']})")


if __name__ == "__main__":
    asyncio.run(main())
