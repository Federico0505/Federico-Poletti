import asyncio
import time
import logging
from typing import Dict, List, Set, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)

class OptimizedScraper:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.action_chains = ActionChains(driver)
        
    async def scrape_category(self, category: Dict) -> List[Dict]:
        """Scrape di tutti i prodotti di una categoria con scroll infinito ottimizzato"""
        logger.info(f"Scraping categoria: {category['name']} - {category['url']}")
        all_products = []
        products_ids = set()  # Per evitare duplicati
        
        try:
            # Carica la pagina iniziale una sola volta
            await self._load_page_with_retry(category['url'])
            
            # Gestisci cookie se necessario
            self.handle_cookies()
            
            # Attendi che i prodotti siano caricati
            await self.wait_for_products()
            
        except Exception as e:
            logger.error(f"Errore nel caricare la categoria {category['name']}: {e}")
            return []
        
        # Variabili per il controllo dello scroll infinito
        last_product_count = 0
        no_new_products_count = 0
        max_no_new_products = 3
        consecutive_failures = 0
        max_consecutive_failures = 2
        
        while no_new_products_count < max_no_new_products and consecutive_failures < max_consecutive_failures:
            try:
                # Prima estrai i prodotti già visibili
                current_products = await self._extract_products_from_current_view(category, products_ids)
                
                if current_products:
                    all_products.extend(current_products)
                    logger.info(f"  Estratti {len(current_products)} nuovi prodotti")
                    logger.info(f"  Totale prodotti finora: {len(all_products)}")
                    consecutive_failures = 0  # Reset counter on success
                
                # Verifica se ci sono nuovi prodotti con retry logic
                current_count = await self._get_product_count_with_retry()
                
                if current_count == last_product_count:
                    no_new_products_count += 1
                    logger.info(f"Nessun nuovo prodotto caricato (tentativo {no_new_products_count}/{max_no_new_products})")
                else:
                    no_new_products_count = 0
                    last_product_count = current_count
                
                # Prova prima a cliccare "Mostra più" se presente
                if await self._click_show_more_optimized():
                    await asyncio.sleep(2)
                    continue
                
                # Altrimenti usa scroll infinito con backoff strategy
                if not await self._scroll_and_load_more_advanced():
                    logger.info("Non ci sono più prodotti da caricare")
                    break
                    
                # Adaptive delay based on page response
                await self._adaptive_delay()
                
            except Exception as e:
                logger.error(f"Errore durante lo scraping: {e}")
                consecutive_failures += 1
                no_new_products_count += 1
                await asyncio.sleep(2)  # Longer delay on error
        
        logger.info(f"Totale prodotti trovati per {category['name']}: {len(all_products)}")
        return all_products

    async def _load_page_with_retry(self, url: str, max_retries: int = 3) -> None:
        """Carica la pagina con retry logic"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                await asyncio.sleep(3)
                
                # Verifica che la pagina sia caricata correttamente
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                return
                
            except Exception as e:
                logger.warning(f"Tentativo {attempt + 1} fallito per {url}: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(5)

    async def _extract_products_from_current_view(self, category: Dict, existing_ids: Set[str]) -> List[Dict]:
        """Estrae solo i prodotti attualmente visibili che non sono già stati processati"""
        products = []
        
        try:
            # Trova tutti i prodotti attualmente nel DOM con retry per elementi stale
            product_elements = await self._get_product_elements_with_retry()
            
            # Process products in batches to avoid memory issues
            batch_size = 50
            for i in range(0, len(product_elements), batch_size):
                batch = product_elements[i:i + batch_size]
                
                for elem in batch:
                    try:
                        # Controlla se l'elemento è ancora valido
                        if not self._is_element_valid(elem):
                            continue
                            
                        # Controlla se il prodotto è già stato processato
                        product_id = elem.get_attribute('data-pid')
                        if product_id and product_id not in existing_ids:
                            product = await self._parse_product_element_safe(elem, category)
                            if product:
                                products.append(product)
                                existing_ids.add(product_id)
                                
                    except StaleElementReferenceException:
                        logger.debug("Elemento stale ignorato")
                        continue
                    except Exception as e:
                        logger.debug(f"Errore nel processare elemento: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Errore nell'estrazione prodotti: {e}")
            
        return products

    async def _get_product_elements_with_retry(self, max_retries: int = 3):
        """Ottiene gli elementi prodotto con retry per gestire elementi stale"""
        for attempt in range(max_retries):
            try:
                return self.driver.find_elements(By.CSS_SELECTOR, ".product[data-pid]")
            except StaleElementReferenceException:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(0.5)

    async def _get_product_count_with_retry(self, max_retries: int = 3) -> int:
        """Ottiene il conteggio dei prodotti con retry logic"""
        for attempt in range(max_retries):
            try:
                return len(self.driver.find_elements(By.CSS_SELECTOR, ".product[data-pid]"))
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.warning(f"Impossibile ottenere il conteggio prodotti: {e}")
                    return 0
                await asyncio.sleep(0.5)

    def _is_element_valid(self, element) -> bool:
        """Verifica se un elemento è ancora valido nel DOM"""
        try:
            element.is_displayed()
            return True
        except StaleElementReferenceException:
            return False
        except Exception:
            return False

    async def _parse_product_element_safe(self, elem, category: Dict) -> Optional[Dict]:
        """Parse sicuro di un elemento prodotto con gestione errori"""
        try:
            # Implementa qui la logica di parsing specifica per il tuo sito
            # Questo è un esempio generico
            return {
                'id': elem.get_attribute('data-pid'),
                'name': self._safe_get_text(elem, '.product-name'),
                'price': self._safe_get_text(elem, '.product-price'),
                'url': self._safe_get_attribute(elem, 'a', 'href'),
                'image': self._safe_get_attribute(elem, 'img', 'src'),
                'category': category['name']
            }
        except Exception as e:
            logger.debug(f"Errore nel parsing prodotto: {e}")
            return None

    def _safe_get_text(self, parent_elem, selector: str) -> str:
        """Ottiene il testo da un elemento in modo sicuro"""
        try:
            elem = parent_elem.find_element(By.CSS_SELECTOR, selector)
            return elem.text.strip()
        except:
            return ""

    def _safe_get_attribute(self, parent_elem, selector: str, attribute: str) -> str:
        """Ottiene un attributo da un elemento in modo sicuro"""
        try:
            elem = parent_elem.find_element(By.CSS_SELECTOR, selector)
            return elem.get_attribute(attribute) or ""
        except:
            return ""

    async def _click_show_more_optimized(self) -> bool:
        """Clicca sul pulsante 'Mostra più' con strategia migliorata"""
        try:
            show_more_selectors = [
                "button.show-more",
                ".show-more-button", 
                "button[class*='show-more']",
                ".load-more",
                "button[data-action='show-more']",
                "a[class*='load-more']",
                ".pagination-next",
                "button[aria-label*='more']"
            ]
            
            for selector in show_more_selectors:
                try:
                    # Usa WebDriverWait per attendere che l'elemento sia cliccabile
                    button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    if button.is_displayed() and button.is_enabled():
                        # Scrolla fino al pulsante per assicurarsi che sia visibile
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
                            button
                        )
                        await asyncio.sleep(0.5)
                        
                        # Prova prima il click normale, poi JavaScript
                        try:
                            button.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", button)
                            
                        logger.info("  Cliccato pulsante 'Mostra più'")
                        await asyncio.sleep(2)
                        
                        # Verifica che il click abbia avuto effetto
                        await self._wait_for_new_content()
                        return True
                        
                except TimeoutException:
                    continue
                except Exception as e:
                    logger.debug(f"Errore con selettore {selector}: {e}")
                    continue
                    
            return False
        except Exception as e:
            logger.debug(f"Errore generale in _click_show_more_optimized: {e}")
            return False

    async def _wait_for_new_content(self, timeout: int = 5) -> None:
        """Attende che nuovo contenuto sia caricato dopo un'azione"""
        try:
            # Attendi che eventuali loader scompaiano
            loader_selectors = [".loader", ".loading", ".spinner", "[data-loading]"]
            for selector in loader_selectors:
                try:
                    WebDriverWait(self.driver, timeout).until(
                        EC.invisibility_of_element_located((By.CSS_SELECTOR, selector))
                    )
                except TimeoutException:
                    continue
        except Exception:
            pass

    async def _scroll_and_load_more_advanced(self) -> bool:
        """Scrolla per caricare più prodotti con strategia avanzata"""
        try:
            # Ottieni l'altezza corrente della pagina
            initial_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Strategia di scroll progressivo con velocità adattiva
            current_position = self.driver.execute_script("return window.pageYOffset")
            scroll_increment = 300  # Scroll più piccolo per trigger migliore del lazy loading
            scroll_pause = 0.2  # Pausa più breve tra gli scroll
            
            # Scrolla gradualmente verso il basso
            while current_position < initial_height - 500:
                # Scroll smooth per non sovraccaricare il browser
                target_position = min(current_position + scroll_increment, initial_height)
                self.driver.execute_script(f"window.scrollTo({{top: {target_position}, behavior: 'smooth'}});")
                
                await asyncio.sleep(scroll_pause)
                current_position = target_position
                
                # Controlla se sono stati caricati nuovi elementi durante lo scroll
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height > initial_height:
                    logger.info("  Nuovi prodotti caricati durante lo scroll graduale")
                    initial_height = new_height
            
            # Scroll finale per triggerare il lazy loading
            self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
            await asyncio.sleep(2)
            
            # Attendi che eventuali nuovi contenuti siano caricati
            await self._wait_for_new_content()
            
            # Verifica se ci sono stati cambiamenti
            final_height = self.driver.execute_script("return document.body.scrollHeight")
            has_new_content = final_height > initial_height
            
            if has_new_content:
                logger.info(f"  Altezza pagina aumentata: {initial_height} -> {final_height}")
            
            return has_new_content
            
        except Exception as e:
            logger.error(f"Errore durante lo scroll avanzato: {e}")
            return False

    async def _adaptive_delay(self) -> None:
        """Delay adattivo basato sulla velocità di risposta della pagina"""
        try:
            # Misura il tempo di risposta della pagina
            start_time = time.time()
            self.driver.execute_script("return document.readyState")
            response_time = time.time() - start_time
            
            # Calcola delay basato sulla risposta (più lenta la pagina, più lungo il delay)
            base_delay = 1.0
            adaptive_delay = base_delay + min(response_time * 2, 3.0)  # Max 4 secondi
            
            await asyncio.sleep(adaptive_delay)
            
        except Exception:
            # Fallback a delay fisso
            await asyncio.sleep(1.5)

    async def wait_for_products(self, timeout: int = 15) -> None:
        """Attende che i prodotti siano caricati con timeout adattivo e retry"""
        try:
            # Attendi che almeno un prodotto sia visibile
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product[data-pid]"))
            )
            
            # Attendi che il DOM sia stabile (nessun cambio per 1 secondo)
            await self._wait_for_dom_stability()
            
            # Attendi che eventuali loader scompaiano
            await self._wait_for_new_content()
            
            logger.info("Prodotti caricati e pagina stabilizzata")
            
        except TimeoutException:
            logger.warning(f"Timeout nell'attesa dei prodotti dopo {timeout} secondi")
            # Prova selettori alternativi
            alternative_selectors = [".product", "[data-product-id]", ".item", ".card"]
            for selector in alternative_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        logger.info(f"Trovati {len(elements)} elementi con selettore alternativo: {selector}")
                        return
                except:
                    continue
            raise

    async def _wait_for_dom_stability(self, stability_time: float = 1.0, max_wait: int = 10) -> None:
        """Attende che il DOM sia stabile (nessun cambiamento per un periodo specificato)"""
        try:
            start_time = time.time()
            last_product_count = 0
            stable_since = time.time()
            
            while time.time() - start_time < max_wait:
                current_count = len(self.driver.find_elements(By.CSS_SELECTOR, ".product[data-pid]"))
                
                if current_count == last_product_count:
                    if time.time() - stable_since >= stability_time:
                        logger.debug("DOM stabile raggiunto")
                        return
                else:
                    last_product_count = current_count
                    stable_since = time.time()
                
                await asyncio.sleep(0.2)
                
        except Exception as e:
            logger.debug(f"Errore nell'attesa stabilità DOM: {e}")

    def handle_cookies(self) -> None:
        """Gestisce i cookie banner con selettori multipli"""
        cookie_selectors = [
            "#cookie-accept",
            ".cookie-accept",
            "button[data-accept-cookies]",
            ".accept-cookies",
            "#accept-all-cookies",
            ".gdpr-accept",
            "button[aria-label*='accept']",
            ".cookie-banner button:first-child"
        ]
        
        for selector in cookie_selectors:
            try:
                cookie_button = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                cookie_button.click()
                logger.info("Cookie banner gestito")
                time.sleep(1)
                return
            except (TimeoutException, NoSuchElementException):
                continue
        
        logger.debug("Nessun cookie banner trovato o gestito")