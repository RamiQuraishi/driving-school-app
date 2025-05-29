#!/usr/bin/env python3
"""
Script to scrape competitor features from driving school management system websites.
"""

import asyncio
import csv
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CompetitorFeature(BaseModel):
    """Model for competitor feature data."""
    competitor: str
    feature: str
    category: str
    description: str
    url: str
    last_updated: datetime
    source: str

class CompetitorScraper:
    """Class for scraping competitor features."""
    
    def __init__(self):
        self.features: List[CompetitorFeature] = []
        self.competitors = {
            "Young Drivers": "https://www.yd.com",
            "AMB Driving": "https://www.ambdriving.com",
            "DriveWise": "https://www.drivewise.com"
        }
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetch webpage content."""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                logger.error(f"Failed to fetch {url}: {response.status}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_features(self, html: str, competitor: str, url: str) -> List[CompetitorFeature]:
        """Parse features from HTML content."""
        features = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Example parsing logic - adjust based on actual website structure
        feature_sections = soup.find_all('div', class_='feature-section')
        
        for section in feature_sections:
            category = section.find('h2').text.strip()
            feature_items = section.find_all('div', class_='feature-item')
            
            for item in feature_items:
                feature = CompetitorFeature(
                    competitor=competitor,
                    feature=item.find('h3').text.strip(),
                    category=category,
                    description=item.find('p').text.strip(),
                    url=url,
                    last_updated=datetime.now(),
                    source="Website"
                )
                features.append(feature)
        
        return features
    
    async def scrape_competitor(self, session: aiohttp.ClientSession, name: str, url: str):
        """Scrape features from a competitor's website."""
        logger.info(f"Scraping {name}...")
        
        html = await self.fetch_page(session, url)
        if html:
            features = self.parse_features(html, name, url)
            self.features.extend(features)
            logger.info(f"Found {len(features)} features for {name}")
    
    async def scrape_all(self):
        """Scrape features from all competitors."""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.scrape_competitor(session, name, url)
                for name, url in self.competitors.items()
            ]
            await asyncio.gather(*tasks)
    
    def save_to_csv(self, filename: str):
        """Save features to CSV file."""
        df = pd.DataFrame([f.dict() for f in self.features])
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(self.features)} features to {filename}")
    
    def save_to_json(self, filename: str):
        """Save features to JSON file."""
        with open(filename, 'w') as f:
            json.dump([f.dict() for f in self.features], f, indent=2, default=str)
        logger.info(f"Saved {len(self.features)} features to {filename}")
    
    def generate_report(self, filename: str):
        """Generate a feature comparison report."""
        df = pd.DataFrame([f.dict() for f in self.features])
        
        # Create pivot table
        pivot = pd.pivot_table(
            df,
            values='feature',
            index='category',
            columns='competitor',
            aggfunc='count',
            fill_value=0
        )
        
        # Save to Excel
        with pd.ExcelWriter(filename) as writer:
            pivot.to_excel(writer, sheet_name='Feature Comparison')
            df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        logger.info(f"Generated report: {filename}")

async def main():
    """Main function."""
    scraper = CompetitorScraper()
    
    # Create output directory
    os.makedirs('docs/competitor_analysis', exist_ok=True)
    
    # Scrape features
    await scraper.scrape_all()
    
    # Save results
    scraper.save_to_csv('docs/competitor_analysis/feature_data.csv')
    scraper.save_to_json('docs/competitor_analysis/feature_data.json')
    scraper.generate_report('docs/competitor_analysis/feature_comparison.xlsx')

if __name__ == "__main__":
    asyncio.run(main()) 