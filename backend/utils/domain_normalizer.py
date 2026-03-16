"""
Domain Normalization Utility for BeScraped
Purpose: Normalize company domains to a consistent format
Author: BeScraped Team
"""

from urllib.parse import urlparse


def normalize_domain(domain: str) -> str:
    """
    Normalizes a domain to a consistent format.

    Input examples:
    - http://example.com
    - https://example.com/
    - www.example.com
    - example.com/contact
    -   https://www.example.co.uk/path?query=1

    Output:
    - example.com
    - example.co.uk
    """
    if not domain:
        return ""

    # Trim whitespace
    domain = domain.strip()

    # If it starts with something that looks like a protocol, parse it
    if domain.startswith("http://") or domain.startswith("https://"):
        try:
            parsed = urlparse(domain)
            domain = parsed.netloc
        except Exception:
            pass
    else:
        # If no protocol, check if it has www prefix
        pass

    # Remove www prefix (including www1, www2, etc.)
    if domain.startswith("www."):
        domain = domain[4:]

    # Remove any port numbers
    if ":" in domain:
        domain = domain.split(":")[0]

    # Remove trailing slash
    if domain.endswith("/"):
        domain = domain[:-1]

    # Remove any path, query parameters, or fragments
    if "/" in domain:
        domain = domain.split("/")[0]
    if "?" in domain:
        domain = domain.split("?")[0]
    if "#" in domain:
        domain = domain.split("#")[0]

    # Convert to lowercase
    domain = domain.lower()

    return domain


def validate_domain(domain: str) -> bool:
    """
    Validates if a domain is in a valid format.

    Returns:
    - True if domain is valid
    - False if domain is invalid
    """
    if not domain or len(domain) < 3:
        return False

    # Check for invalid characters
    invalid_chars = [" ", "@", "!", "$", "%", "^", "&", "*", "(", ")", "=", "+", "[", "]", "{", "}", "|", "\\", ";", ":", "\"", "'", "<", ">", "?", "/"]
    for char in invalid_chars:
        if char in domain:
            return False

    # Check if it has at least one dot
    if "." not in domain:
        return False

    # Check if it starts or ends with invalid characters
    if domain.startswith(".") or domain.endswith("."):
        return False

    return True


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "http://example.com",
        "https://example.com/",
        "www.example.com",
        "example.com/contact",
        "   https://www.example.co.uk/path?query=1  ",
        "http://localhost:3000",
        "example.org",
        "www1.example.net",
        "invalid domain",
        "example..com",
        ".example.com",
        "example.com.",
        "example"
    ]

    print("Domain Normalization Test Cases:")
    print("-" * 50)
    for test in test_cases:
        normalized = normalize_domain(test)
        valid = validate_domain(normalized)
        print(f"Input: '{test}'")
        print(f"Normalized: '{normalized}'")
        print(f"Valid: {valid}")
        print()
