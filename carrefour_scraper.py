import asyncio
import time
import logging
from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up logging
logger = logging.getLogger(__name__)

class CarrefourScraper:
    def __init__(self, driver):
        self.driver = driver

    async def scrape_category(self, category: Dict) -> List[Dict]:
        """Scrape di tutti i prodotti di una categoria con scroll infinito ottimizzato"""
        logger.info(f"Scraping categoria: {category['name']} - {category['url']}")
        all_products = []
        products_ids = set()  # Per evitare duplicati
        
        try:
            # Carica la pagina iniziale una sola volta
            self.driver.get(category['url'])
            time.sleep(3)
            
            # Gestisci cookie se necessario
            self.handle_cookies()
            
            # Attendi che i prodotti siano caricati
            self.wait_for_products()
            
        except Exception as e:
            logger.error(f"Errore nel caricare la categoria {category['name']}: {e}")
            return []
        
        # Variabili per il controllo dello scroll infinito
        last_product_count = 0
        no_new_products_count = 0
        max_no_new_products = 3
        
        while no_new_products_count < max_no_new_products:
            try:
                # Prima estrai i prodotti già visibili
                current_products = self._extract_products_from_current_view(category, products_ids)
                
                if current_products:
                    all_products.extend(current_products)
                    logger.info(f"  Estratti {len(current_products)} nuovi prodotti")
                    logger.info(f"  Totale prodotti finora: {len(all_products)}")
                
                # Verifica se ci sono nuovi prodotti
                current_count = len(self.driver.find_elements(By.CSS_SELECTOR, ".product[data-pid]"))
                if current_count == last_product_count:
                    no_new_products_count += 1
                    logger.info(f"Nessun nuovo prodotto caricato (tentativo {no_new_products_count}/{max_no_new_products})")
                else:
                    no_new_products_count = 0
                    last_product_count = current_count
                
                # Prova prima a cliccare "Mostra più" se presente
                if self._click_show_more_optimized():
                    time.sleep(2)
                    continue
                
                # Altrimenti usa scroll infinito
                if not self._scroll_and_load_more():
                    logger.info("Non ci sono più prodotti da caricare")
                    break
                    
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Errore durante lo scraping: {e}")
                no_new_products_count += 1
        
        logger.info(f"Totale prodotti trovati per {category['name']}: {len(all_products)}")
        return all_products

    def _extract_products_from_current_view(self, category: Dict, existing_ids: set) -> List[Dict]:
        """Estrae solo i prodotti attualmente visibili che non sono già stati processati"""
        products = []
        
        try:
            # Trova tutti i prodotti attualmente nel DOM
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product[data-pid]")
            
            for elem in product_elements:
                try:
                    # Controlla se il prodotto è già stato processato
                    product_id = elem.get_attribute('data-pid')
                    if product_id and product_id not in existing_ids:
                        product = self._parse_product_element(elem, category)
                        if product:
                            products.append(product)
                            existing_ids.add(product_id)
                except Exception as e:
                    continue
                    
        except Exception as e:
            logger.error(f"Errore nell'estrazione prodotti: {e}")
            
        return products

    def _click_show_more_optimized(self) -> bool:
        """Clicca sul pulsante 'Mostra più' senza ricaricare la pagina"""
        try:
            show_more_selectors = [
                "button.show-more",
                ".show-more-button", 
                "button[class*='show-more']",
                ".load-more",
                "button[data-action='show-more']"
            ]
            
            for selector in show_more_selectors:
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if button.is_displayed() and button.is_enabled():
                        # Scrolla fino al pulsante per assicurarsi che sia visibile
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                        time.sleep(0.5)
                        
                        # Clicca usando JavaScript per evitare problemi di intercettazione
                        self.driver.execute_script("arguments[0].click();", button)
                        logger.info("  Cliccato pulsante 'Mostra più'")
                        time.sleep(2)
                        return True
                except:
                    continue
                    
            return False
        except:
            return False

    def _scroll_and_load_more(self) -> bool:
        """Scrolla per caricare più prodotti con lazy loading"""
        try:
            # Ottieni l'altezza corrente della pagina
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scrolla gradualmente verso il basso
            current_position = self.driver.execute_script("return window.pageYOffset")
            scroll_increment = 500
            
            # Scrolla fino alla fine della pagina corrente
            while current_position < last_height - 1000:
                current_position += scroll_increment
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(0.3)
                
                # Verifica se sono stati caricati nuovi elementi durante lo scroll
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    logger.info("  Nuovi prodotti caricati durante lo scroll")
                    last_height = new_height
            
            # Scroll finale per triggerare il lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Verifica se ci sono stati cambiamenti
            final_height = self.driver.execute_script("return document.body.scrollHeight")
            return final_height > last_height
            
        except Exception as e:
            logger.error(f"Errore durante lo scroll: {e}")
            return False

    def wait_for_products(self):
        """Attende che i prodotti siano caricati con timeout adattivo"""
        try:
            # Attendi che almeno un prodotto sia visibile
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product[data-pid]"))
            )
            
            # Attendi che il loader scompaia (se presente)
            try:
                loader = self.driver.find_element(By.CSS_SELECTOR, ".loader")
                WebDriverWait(self.driver, 5).until(EC.invisibility_of_element(loader))
            except:
                pass
                
            # Breve pausa per assicurarsi che il rendering sia completo
            time.sleep(1)
            
        except TimeoutException:
            logger.warning("Timeout nell'attesa dei prodotti")

    def handle_cookies(self):
        """Handle cookie consent if present"""
        try:
            # Common cookie consent selectors
            cookie_selectors = [
                "button[id*='cookie']",
                "button[class*='cookie']",
                ".cookie-accept",
                "#cookie-accept",
                "button[data-action='accept-cookies']"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if cookie_button.is_displayed():
                        cookie_button.click()
                        logger.info("Cookie consent handled")
                        time.sleep(1)
                        return
                except:
                    continue
        except:
            pass

    def _parse_product_element(self, elem, category: Dict) -> Dict:
        """Parse a product element and extract product information"""
        # This method needs to be implemented based on the specific HTML structure
        # of the Carrefour website. Here's a placeholder implementation:
        try:
            product = {
                'id': elem.get_attribute('data-pid'),
                'category': category['name'],
                'url': category['url']
            }
            
            # Add more parsing logic here based on the actual HTML structure
            # For example:
            # product['name'] = elem.find_element(By.CSS_SELECTOR, '.product-name').text
            # product['price'] = elem.find_element(By.CSS_SELECTOR, '.price').text
            # etc.
            
            return product
        except Exception as e:
            logger.error(f"Error parsing product element: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Example of how to use the scraper
    # You'll need to initialize your WebDriver and create category objects
    # 
    # driver = webdriver.Chrome()  # or your preferred driver
    # scraper = CarrefourScraper(driver)
    # 
    # category = {
    #     'name': 'Example Category',
    #     'url': 'https://example.com/category'
    # }
    # 
    # products = asyncio.run(scraper.scrape_category(category))
    # print(f"Found {len(products)} products")
    
    print("Carrefour scraper module loaded successfully!")