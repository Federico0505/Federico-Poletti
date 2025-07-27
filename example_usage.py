#!/usr/bin/env python3
"""
Example usage of the CarrefourScraper class.

This script demonstrates how to use the scraper to extract products from Carrefour categories.
Make sure you have a WebDriver installed (e.g., ChromeDriver) before running this script.
"""

import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from carrefour_scraper import CarrefourScraper

def setup_driver():
    """Set up and return a configured WebDriver instance."""
    chrome_options = Options()
    
    # Add options for better scraping performance
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Disable images and CSS for faster loading
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Make sure ChromeDriver is installed and in your PATH")
        return None

async def main():
    """Main function to demonstrate scraper usage."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set up the WebDriver
    driver = setup_driver()
    if not driver:
        return
    
    try:
        # Create scraper instance
        scraper = CarrefourScraper(driver)
        
        # Example categories to scrape
        # You'll need to replace these with actual Carrefour category URLs
        categories = [
            {
                'name': 'Fruits et Légumes',
                'url': 'https://www.carrefour.fr/magasin/fruits-et-legumes'
            },
            {
                'name': 'Produits Laitiers',
                'url': 'https://www.carrefour.fr/magasin/produits-laitiers'
            }
        ]
        
        all_products = []
        
        # Scrape each category
        for category in categories:
            print(f"\n🔍 Starting to scrape category: {category['name']}")
            products = await scraper.scrape_category(category)
            all_products.extend(products)
            print(f"✅ Found {len(products)} products in {category['name']}")
        
        print(f"\n🎉 Total products scraped: {len(all_products)}")
        
        # Save results to file (optional)
        if all_products:
            import json
            with open('scraped_products.json', 'w', encoding='utf-8') as f:
                json.dump(all_products, f, indent=2, ensure_ascii=False)
            print("📁 Results saved to 'scraped_products.json'")
        
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
    finally:
        # Always close the driver
        driver.quit()
        print("🔒 Browser closed")

if __name__ == "__main__":
    print("🚀 Starting Carrefour Scraper Example")
    print("=" * 50)
    
    # Check if running in async context
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("=" * 50)
    print("✨ Scraping completed")