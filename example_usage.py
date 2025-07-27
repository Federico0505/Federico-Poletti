#!/usr/bin/env python3
"""
Esempio di utilizzo dello scraper ottimizzato per e-commerce
"""

import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper_optimized import OptimizedScraper

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """Configura il driver Chrome con opzioni ottimizzate per lo scraping"""
    chrome_options = Options()
    
    # Opzioni per performance e stabilità
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Gestione memoria
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    
    # Disabilita immagini per velocizzare (opzionale)
    # chrome_options.add_argument("--disable-images")
    
    # User agent realistico
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Finestra nascosta (opzionale)
    # chrome_options.add_argument("--headless")
    
    # Dimensioni finestra
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Prefs per disabilitare notifiche e popup
    prefs = {
        "profile.default_content_setting_values": {
            "notifications": 2,
            "geolocation": 2,
            "media_stream": 2,
        },
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Timeout per page load
    chrome_options.add_argument("--page-load-strategy=eager")
    
    return webdriver.Chrome(options=chrome_options)

async def scrape_multiple_categories(categories):
    """Esegue lo scraping di multiple categorie in modo sequenziale"""
    driver = None
    all_results = {}
    
    try:
        # Setup driver
        logger.info("Inizializzazione driver Chrome...")
        driver = setup_chrome_driver()
        driver.implicitly_wait(10)
        
        # Inizializza scraper
        scraper = OptimizedScraper(driver)
        
        # Scraping delle categorie
        for i, category in enumerate(categories, 1):
            logger.info(f"\n=== Scraping categoria {i}/{len(categories)}: {category['name']} ===")
            
            try:
                products = await scraper.scrape_category(category)
                all_results[category['name']] = products
                
                logger.info(f"✅ Completato scraping {category['name']}: {len(products)} prodotti")
                
                # Pausa tra le categorie per evitare rate limiting
                if i < len(categories):
                    logger.info("Pausa tra categorie...")
                    await asyncio.sleep(5)
                    
            except Exception as e:
                logger.error(f"❌ Errore scraping categoria {category['name']}: {e}")
                all_results[category['name']] = []
                continue
        
        return all_results
        
    except Exception as e:
        logger.error(f"Errore generale durante lo scraping: {e}")
        return {}
        
    finally:
        if driver:
            logger.info("Chiusura driver...")
            driver.quit()

def save_results_to_json(results, filename="scraping_results.json"):
    """Salva i risultati in formato JSON"""
    import json
    from datetime import datetime
    
    # Aggiungi metadata
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_categories": len(results),
        "total_products": sum(len(products) for products in results.values()),
        "categories": results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Risultati salvati in {filename}")

def save_results_to_csv(results, filename="scraping_results.csv"):
    """Salva i risultati in formato CSV"""
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if not results:
            return
            
        # Ottieni tutti i prodotti per determinare le colonne
        all_products = []
        for category_name, products in results.items():
            for product in products:
                product['scraped_category'] = category_name
                all_products.append(product)
        
        if not all_products:
            return
            
        # Determina le colonne
        fieldnames = set()
        for product in all_products:
            fieldnames.update(product.keys())
        fieldnames = sorted(list(fieldnames))
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products)
    
    logger.info(f"Risultati salvati in {filename}")

async def main():
    """Funzione principale"""
    
    # Definisci le categorie da scrapare
    categories = [
        {
            "name": "Elettronica",
            "url": "https://example-ecommerce.com/elettronica"
        },
        {
            "name": "Abbigliamento",
            "url": "https://example-ecommerce.com/abbigliamento"
        },
        {
            "name": "Casa e Giardino",
            "url": "https://example-ecommerce.com/casa-giardino"
        }
    ]
    
    logger.info(f"Avvio scraping di {len(categories)} categorie...")
    
    # Esegui lo scraping
    results = await scrape_multiple_categories(categories)
    
    # Statistiche finali
    total_products = sum(len(products) for products in results.values())
    logger.info(f"\n=== RISULTATI FINALI ===")
    logger.info(f"Categorie processate: {len(results)}")
    logger.info(f"Prodotti totali trovati: {total_products}")
    
    for category_name, products in results.items():
        logger.info(f"  - {category_name}: {len(products)} prodotti")
    
    # Salva risultati
    if total_products > 0:
        save_results_to_json(results)
        save_results_to_csv(results)
        logger.info("✅ Scraping completato con successo!")
    else:
        logger.warning("⚠️ Nessun prodotto trovato")

if __name__ == "__main__":
    # Esegui lo scraping
    asyncio.run(main())