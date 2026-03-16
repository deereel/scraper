"""
Database Models for BeScraped
Purpose: Define database schema and models
Author: BeScraped Team
"""

import os
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Text, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '../../database/bescraped.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

Base = declarative_base()


class Company(Base):
    """
    Company table to store scraped company information.
    """
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, nullable=False, index=True)
    company_name = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    executive_first_name = Column(String(100), nullable=True)
    executive_last_name = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Company(domain='{self.domain}', company_name='{self.company_name}')>"

    def to_dict(self):
        """Convert company record to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'domain': self.domain,
            'company_name': self.company_name,
            'address': self.address,
            'executive_first_name': self.executive_first_name,
            'executive_last_name': self.executive_last_name,
            'source': self.source,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ScrapingJob(Base):
    """
    Scraping job table to track scraping tasks.
    """
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    progress = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ScrapingJob(domain='{self.domain}', status='{self.status}')>"


class SourceData(Base):
    """
    Source data table to store raw data from each scraping source.
    """
    __tablename__ = "source_data"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    raw_data = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SourceData(domain='{self.domain}', source='{self.source}')>"


# Database engine and session with larger pool size
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_size=20,
    max_overflow=40,
    pool_timeout=60,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables (for initial setup)."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


def drop_tables():
    """Drop all database tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
    print("All database tables dropped.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        confirm = input("Are you sure you want to drop all tables? (y/n): ").strip().lower()
        if confirm == "y":
            drop_tables()
    else:
        create_tables()
