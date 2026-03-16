"""
HTML Text Cleaner for BeScraped
Purpose: Convert HTML to clean text by removing unwanted elements
Author: BeScraped Team
"""

from bs4 import BeautifulSoup, Comment
from typing import Set


class HTMLTextCleaner:
    """Utility to clean HTML content and extract plain text."""

    def __init__(self):
        """Initialize HTML cleaner with default configuration."""
        self.remove_tags = {
            'script', 'style', 'header', 'footer', 'nav', 'aside', 'iframe', 'noscript'
        }

    def clean_html(self, html_content: str) -> str:
        """
        Clean HTML content and extract plain text.

        Args:
            html_content: Raw HTML content

        Returns:
            Cleaned plain text
        """
        if not html_content:
            return ""

        # Parse HTML
        soup = BeautifulSoup(html_content, 'lxml')

        # Remove unwanted tags
        for tag in self.remove_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove empty tags
        for tag in soup.find_all():
            if len(tag.get_text(strip=True)) == 0:
                tag.extract()

        # Extract text
        text = soup.get_text()

        # Cleanup whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)

        return cleaned_text

    def add_remove_tags(self, tags: Set[str]):
        """
        Add tags to the list of tags to remove.

        Args:
            tags: Set of tag names to add to removal list
        """
        self.remove_tags.update(tags)

    def remove_remove_tags(self, tags: Set[str]):
        """
        Remove tags from the list of tags to remove.

        Args:
            tags: Set of tag names to remove from removal list
        """
        self.remove_tags.difference_update(tags)


def main():
    """Test function."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python html_cleaner.py <html_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        cleaner = HTMLTextCleaner()
        cleaned_text = cleaner.clean_html(html_content)

        print("Cleaned text:")
        print("-" * 50)
        print(cleaned_text)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
