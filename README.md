<p align="center">
  <img alt="Logo" src="assets/icon/ont_logo_square.png" width="128" />
  <h1 align="center">OpenNutriTracker</h1>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT" alt="License">
        <img src="https://img.shields.io/badge/license-GPLv3-blue" /></a>
  <a href="https://github.com/simonoppowa/OpenNutriTracker/stargazers" alt="GitHub Stars">
        <img src="https://img.shields.io/github/stars/simonoppowa/OpenNutriTracker.svg" /></a>
  <a href="https://github.com/simonoppowa/OpenNutriTracker/issues" alt="GitHub Issues">
        <img src="https://img.shields.io/github/issues/simonoppowa/OpenNutriTracker.svg" /></a>
  <a href="https://github.com/simonoppowa/OpenNutriTracker/pulls" alt="GitHub Pull Requests">
        <img src="https://img.shields.io/github/issues-pr/simonoppowa/OpenNutriTracker.svg" /></a>
  <a alt="Version">
        <img src="https://img.shields.io/badge/version-alpha-orange.svg" /></a>
</p>

## Description
OpenNutriTracker is an open-source mobile application designed to simplify nutritional tracking and management. Whether you are looking to improve your health, lose weight, or simply maintain a balanced diet, OpenNutriTracker provides a minimalistic interface to easily track and analyze your daily nutrition.

[Website](https://simonoppowa.github.io/OpenNutriTracker-Website/)

## Screenshots
<p align="center">
  <img alt="Logo" src="fastlane/metadata/android/en-US/images/phoneScreenshots/1_en-US.png" width="20%" />
  &nbsp;&nbsp;
  <img alt="Logo" src="fastlane/metadata/android/en-US/images/phoneScreenshots/2_en-US.png" width="20%" />
  &nbsp;&nbsp;
  <img alt="Logo" src="fastlane/metadata/android/en-US/images/phoneScreenshots/3_en-US.png" width="20%" />
  &nbsp;&nbsp;
  <img alt="Logo" src="fastlane/metadata/android/en-US/images/phoneScreenshots/4_en-US.png" width="20%" />
</p>

## Install
[<img src="fastlane/metadata/android/en-US/images/appstore_banner.png" width="30%">](https://testflight.apple.com/join/j7uKoEDl)
[<img src="fastlane/metadata/android/en-US/images/playstore_banner.png" width="30%">](https://play.google.com/store/apps/details?id=com.opennutritracker.ont.opennutritracker)

## Key Features
- **🍎 Nutritional Tracking:** Easily log your meals and snacks, and access a vast database of food items and ingredients to get detailed nutritional information.
- **📓 Food Diary:** Maintain a comprehensive food diary to keep track of your daily food consumption, habits, and progress.
- **🍽️ Custom Meals:** Plan your meals in advance, create personalized meal plans, and optimize them according to your dietary goals.
- **📷 Barcode Scanner:** Scan barcodes on packaged food items to instantly retrieve their nutritional information.
- **🔒 Privacy Focused:** OpenNutriTracker prioritizes the privacy its users. It does not collect or share any personal data without your consent.
- **🚫💰 No Subscription, In-App Purchases, or Ads:** OpenNutriTracker is completely free to use, without any subscription fees, in-app purchases, or intrusive advertisements.

## Privacy
See [Data Protection](https://www.iubenda.com/privacy-policy/53501884)
- **Data Encryption**: All collected user data is encrypted and stored locally on your device
- **Minimal Data Collection**: OpenNutriTracker only collects the necessary information required for tracking nutrition and providing personalized insights. Your data will not be shared with third parties without your consent.
- **Open-Source**: OpenNutriTracker is an open-source application

## TODOs
- Add serving sizes to meals
- Add Imperial unit support
- Add support for Material You themes

## Contribution
Contributions to OpenNutriTracker are welcome! If you find any issues or have suggestions for new features, please open an issue or submit a pull request. Make sure to follow the project's code style and guidelines.

## Disclaimer
OpenNutriTracker is not a medical application. All data provided is not validated and should be used with caution. Please maintain a healthy lifestyle and consult a professional if you have any problems. Use during illness, pregnancy or lactation is not recommended.

The application is still under construction. Errors, bugs and crashes might occur.

## Acknowledgments
The OpenNutriTracker project was inspired by the need for a simple and effective nutrition tracking tool.
The food database used in OpenNutriTracker is powered by [Open Food Facts](https://world.openfoodfacts.org/) and [Food Data Central](https://fdc.nal.usda.gov/).

## License
This project is licensed under the GNU General Public License v3.0 License. See the [LICENSE](LICENSE) file for more information.

## Contact
For questions, suggestions, or collaborations, feel free to contact the project maintainer:

Simon Oppowa

- GitHub: [@simonoppowa](https://github.com/simonoppowa)
- Email: [opennutritracker-dev@pm.me](mailto:opennutritracker-dev@pm.me)

# Scraper E-commerce Ottimizzato

Un web scraper avanzato per siti e-commerce con scroll infinito, ottimizzato per performance, affidabilità e gestione degli errori.

## 🚀 Caratteristiche Principali

### Miglioramenti Rispetto alla Versione Originale

1. **Gestione Avanzata degli Errori**
   - Retry logic per operazioni critiche
   - Gestione elementi DOM stale
   - Recupero automatico da errori temporanei
   - Timeout adattivi

2. **Performance Ottimizzate**
   - Processing dei prodotti in batch
   - Scroll progressivo intelligente
   - Delay adattivi basati sulla risposta del server
   - Gestione memoria migliorata

3. **Stabilità Migliorata**
   - Attesa stabilità DOM
   - Verifica validità elementi
   - Gestione cookie banner avanzata
   - Selettori multipli per maggiore compatibilità

4. **Async/Await Completo**
   - Operazioni completamente asincrone
   - Migliore gestione concorrenza
   - Performance superiori

## 📦 Installazione

```bash
# Clona il repository
git clone <repository-url>
cd scraper-ecommerce

# Installa le dipendenze
pip install -r requirements.txt

# Installa ChromeDriver (se non già presente)
# Su Ubuntu/Debian:
sudo apt-get install chromium-chromedriver

# Su macOS:
brew install chromedriver

# Su Windows, scarica da: https://chromedriver.chromium.org/
```

## 🛠️ Configurazione

### 1. Personalizza i Selettori CSS

Nel file `scraper_optimized.py`, modifica i selettori CSS nella funzione `_parse_product_element_safe()` per adattarli al tuo sito target:

```python
def _parse_product_element_safe(self, elem, category: Dict) -> Optional[Dict]:
    return {
        'id': elem.get_attribute('data-pid'),
        'name': self._safe_get_text(elem, '.your-product-name-selector'),
        'price': self._safe_get_text(elem, '.your-price-selector'),
        'url': self._safe_get_attribute(elem, 'a', 'href'),
        'image': self._safe_get_attribute(elem, 'img', 'src'),
        'category': category['name']
    }
```

### 2. Configura le Categorie

Nel file `example_usage.py`, aggiorna l'array `categories` con le tue URL:

```python
categories = [
    {
        "name": "Elettronica",
        "url": "https://tuo-sito.com/elettronica"
    },
    # Aggiungi altre categorie...
]
```

## 🚀 Utilizzo

### Utilizzo Base

```bash
python example_usage.py
```

### Utilizzo Programmatico

```python
import asyncio
from scraper_optimized import OptimizedScraper
from selenium import webdriver

async def scrape_example():
    driver = webdriver.Chrome()
    scraper = OptimizedScraper(driver)
    
    category = {
        "name": "Test Category",
        "url": "https://example.com/category"
    }
    
    products = await scraper.scrape_category(category)
    
    print(f"Trovati {len(products)} prodotti")
    driver.quit()

# Esegui
asyncio.run(scrape_example())
```

## 🔧 Configurazioni Avanzate

### Opzioni Chrome Driver

Il driver Chrome viene configurato automaticamente con opzioni ottimizzate:

- `--no-sandbox`: Disabilita sandbox per ambienti containerizzati
- `--disable-dev-shm-usage`: Riduce utilizzo memoria condivisa
- `--disable-gpu`: Disabilita accelerazione GPU
- `--memory-pressure-off`: Disabilita gestione pressione memoria
- User-Agent realistico per evitare detection

### Personalizzazione Timeout

```python
# Modifica timeout nel costruttore
scraper = OptimizedScraper(driver)

# Timeout personalizzati
await scraper.wait_for_products(timeout=20)  # 20 secondi invece di 15
```

### Modalità Headless

Per eseguire in background senza interfaccia grafica:

```python
chrome_options.add_argument("--headless")
```

## 📊 Output

### Formato JSON

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "total_categories": 3,
  "total_products": 1250,
  "categories": {
    "Elettronica": [
      {
        "id": "prod123",
        "name": "Smartphone XYZ",
        "price": "€299.99",
        "url": "https://example.com/prod123",
        "image": "https://example.com/img123.jpg",
        "category": "Elettronica"
      }
    ]
  }
}
```

### Formato CSV

Il CSV include tutti i campi dei prodotti con una colonna aggiuntiva `scraped_category`.

## 🐛 Risoluzione Problemi

### Errori Comuni

1. **ChromeDriver non trovato**
   ```bash
   # Installa webdriver-manager
   pip install webdriver-manager
   
   # Usa nel codice:
   from webdriver_manager.chrome import ChromeDriverManager
   driver = webdriver.Chrome(ChromeDriverManager().install())
   ```

2. **Timeout durante il caricamento**
   - Aumenta i timeout nelle configurazioni
   - Verifica la connessione internet
   - Controlla se il sito ha protezioni anti-bot

3. **Elementi non trovati**
   - Verifica i selettori CSS nel browser
   - Controlla se il sito usa lazy loading
   - Aggiungi delay aggiuntivi se necessario

### Debug Avanzato

Abilita logging dettagliato:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 🔒 Best Practices

1. **Rispetta i robots.txt** del sito target
2. **Usa delay appropriati** tra le richieste
3. **Monitora il rate limiting** del server
4. **Implementa retry logic** per operazioni critiche
5. **Gestisci gracefully** gli errori di rete

## 📈 Performance

### Metriche Tipiche

- **Prodotti/minuto**: 200-500 (dipende dal sito)
- **Utilizzo memoria**: ~200-400MB
- **CPU**: Moderato (10-30%)

### Ottimizzazioni Possibili

1. **Disabilita immagini**: `chrome_options.add_argument("--disable-images")`
2. **Usa proxy rotation** per siti con rate limiting
3. **Implementa caching** per evitare re-scraping
4. **Parallelizza** lo scraping di categorie diverse

## 🤝 Contribuire

1. Fork del repository
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

## ⚠️ Disclaimer

Questo strumento è fornito solo per scopi educativi e di ricerca. Assicurati di rispettare i termini di servizio dei siti web che intendi scrapare e le leggi locali applicabili.
