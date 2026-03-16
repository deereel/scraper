"""
Data Merging Engine for BeScraped
Purpose: Combine results from multiple sources with reliability scoring
Author: BeScraped Team
"""

from typing import List, Dict, Optional
from backend.services.confidence_scorer import ConfidenceScorer


class DataMerger:
    """Engine to merge and deduplicate scraped data from multiple sources."""

    def __init__(self):
        """Initialize data merger with confidence scorer."""
        self.scorer = ConfidenceScorer()

    def merge_records(self, records: List[Dict]) -> Dict:
        """
        Merge multiple records for the same domain.

        Args:
            records: List of scraped records for the same domain

        Returns:
            Merged record with highest confidence data for each field
        """
        if not records:
            return {}

        # Calculate confidence scores for all records
        records_with_scores = self.scorer.rank_records_by_confidence(records)

        # Initialize merged record with the highest confidence record as base
        base_record = records_with_scores[0].copy()

        # For each field, find the highest quality value from all sources
        fields = ['company_name', 'address', 'executive_first_name', 'executive_last_name']

        for field in fields:
            best_value = None
            highest_confidence = 0

            for record in records_with_scores:
                value = record.get(field)
                if value and value.strip():
                    # Calculate confidence for this specific field value
                    record_score = self.scorer.calculate_field_score(
                        value,
                        self.scorer.get_source_score(record.get('source', 'Other'))
                    )

                    if record_score > highest_confidence:
                        highest_confidence = record_score
                        best_value = value.strip()

            if best_value:
                base_record[field] = best_value

        # Remove temporary fields
        if 'confidence' in base_record:
            del base_record['confidence']

        # Add merged source information
        sources = list(set(record.get('source', 'Other') for record in records))
        if len(sources) > 1:
            base_record['source'] = 'Multiple Sources'
        elif sources:
            base_record['source'] = sources[0]
        else:
            base_record['source'] = 'Unknown'

        return base_record

    def deduplicate_records(self, records: List[Dict]) -> List[Dict]:
        """
        Deduplicate records by domain.

        Args:
            records: List of scraped records

        Returns:
            Deduplicated list with merged records per domain
        """
        domain_groups = {}

        # Group records by domain
        for record in records:
            domain = record.get('domain', '')
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(record)

        # Merge records within each domain group
        merged_records = []
        for domain, domain_records in domain_groups.items():
            merged_record = self.merge_records(domain_records)
            if merged_record:
                merged_record['domain'] = domain
                merged_records.append(merged_record)

        return merged_records

    def process_scraping_results(self, results: List[Dict]) -> List[Dict]:
        """
        Process scraping results by deduplicating and merging.

        Args:
            results: Raw scraping results from all sources

        Returns:
            Processed and merged results
        """
        # Validate and normalize results
        valid_records = []
        for record in results:
            if self._is_valid_record(record):
                valid_records.append(record)

        # Deduplicate and merge
        return self.deduplicate_records(valid_records)

    def _is_valid_record(self, record: Dict) -> bool:
        """
        Check if a record is valid.

        Args:
            record: Record to check

        Returns:
            True if record is valid, False otherwise
        """
        # Must have a domain
        if not record.get('domain'):
            return False

        # Must have at least one of the main fields
        has_data = any([
            record.get('company_name'),
            record.get('address'),
            record.get('executive_first_name'),
            record.get('executive_last_name')
        ])

        return has_data


def main():
    """Test function."""
    test_records = [
        {
            'domain': 'example.com',
            'company_name': 'Example Limited',
            'address': '123 Main Street, London, SW1A 1AA',
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Companies House'
        },
        {
            'domain': 'example.com',
            'company_name': 'Example Ltd',
            'address': '123 Main St, London',
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Company Website'
        },
        {
            'domain': 'example.com',
            'company_name': 'Example Ltd',
            'address': None,
            'executive_first_name': 'John',
            'executive_last_name': 'Smith',
            'source': 'Google Snippet'
        },
        {
            'domain': 'test.org',
            'company_name': 'Test Organization',
            'address': '456 High Street, Manchester, M1 1AA',
            'executive_first_name': 'Jane',
            'executive_last_name': 'Doe',
            'source': 'Company Website'
        },
        {
            'domain': 'test.org',
            'company_name': 'Test Org Ltd',
            'address': '456 High Street, Manchester, M1 1AA',
            'executive_first_name': 'Jane',
            'executive_last_name': 'Doe',
            'source': 'LinkedIn'
        }
    ]

    merger = DataMerger()
    merged_results = merger.process_scraping_results(test_records)

    print("Merged results:")
    print("-" * 80)

    for i, record in enumerate(merged_results, 1):
        print(f"{i}. Domain: {record['domain']}")
        print(f"   Company Name: {record['company_name']}")
        print(f"   Address: {record['address']}")
        print(f"   Executive: {record['executive_first_name']} {record['executive_last_name']}")
        print(f"   Source: {record['source']}")
        print()


if __name__ == "__main__":
    main()
