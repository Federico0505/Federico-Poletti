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

# Carrefour Scraper

A Python web scraper for extracting product information from Carrefour websites using Selenium with optimized infinite scroll handling.

## Features

- ✅ **Infinite scroll handling**: Automatically handles lazy-loaded content
- ✅ **Duplicate prevention**: Tracks product IDs to avoid duplicates
- ✅ **Optimized scrolling**: Gradual scrolling with smart loading detection
- ✅ **Cookie management**: Automatically handles cookie consent popups
- ✅ **Error handling**: Robust error handling with logging
- ✅ **Async support**: Uses asyncio for better performance
- ✅ **Show more button**: Automatically clicks "Show more" buttons when available

## Installation

1. **Clone or download the files**:
   - `carrefour_scraper.py` - Main scraper class
   - `example_usage.py` - Example usage script
   - `requirements.txt` - Python dependencies

2. **Set up a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ChromeDriver**:
   - Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
   - Make sure it's in your system PATH or specify the path in your code

## Usage

### Basic Usage

```python
import asyncio
from selenium import webdriver
from carrefour_scraper import CarrefourScraper

# Set up WebDriver
driver = webdriver.Chrome()
scraper = CarrefourScraper(driver)

# Define category to scrape
category = {
    'name': 'Example Category',
    'url': 'https://www.carrefour.fr/category-url'
}

# Scrape products
products = asyncio.run(scraper.scrape_category(category))
print(f"Found {len(products)} products")

# Don't forget to close the driver
driver.quit()
```

### Using the Example Script

Run the example script to see the scraper in action:

```bash
python example_usage.py
```

**Note**: You'll need to update the category URLs in `example_usage.py` with actual Carrefour category pages.

## Configuration

### WebDriver Options

The scraper works best with the following Chrome options:

```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run without GUI
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# Disable images for faster loading
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)
```

### Logging

Configure logging to track scraping progress:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
```

## How It Works

1. **Page Loading**: Loads the category page and handles cookie consent
2. **Product Detection**: Waits for products to load using CSS selectors
3. **Scroll Management**: Implements intelligent scrolling with these strategies:
   - First tries to click "Show more" buttons
   - Falls back to gradual scrolling to trigger lazy loading
   - Monitors for new content and stops when no more products load
4. **Data Extraction**: Extracts product information from each product element
5. **Duplicate Prevention**: Uses product IDs to avoid processing the same product twice

## Customization

### Product Parsing

You'll need to implement the `_parse_product_element` method based on the specific HTML structure of the Carrefour website:

```python
def _parse_product_element(self, elem, category: Dict) -> Dict:
    try:
        product = {
            'id': elem.get_attribute('data-pid'),
            'name': elem.find_element(By.CSS_SELECTOR, '.product-name').text,
            'price': elem.find_element(By.CSS_SELECTOR, '.price').text,
            'category': category['name'],
            'url': category['url']
        }
        return product
    except Exception as e:
        logger.error(f"Error parsing product: {e}")
        return None
```

### CSS Selectors

Update the CSS selectors in the code to match the target website's HTML structure:

- Product containers: `.product[data-pid]`
- Show more buttons: `button.show-more`, `.show-more-button`, etc.
- Cookie consent: `button[id*='cookie']`, `.cookie-accept`, etc.

## Error Handling

The scraper includes comprehensive error handling:

- **Network timeouts**: Configurable wait times for page elements
- **Missing elements**: Graceful handling of missing product information
- **Scroll detection**: Automatic detection when no more content is available
- **Driver issues**: Proper cleanup of WebDriver resources

## Legal and Ethical Considerations

⚠️ **Important**: 

- Always check the website's `robots.txt` file and terms of service
- Respect rate limits and don't overload the server
- Consider the website's API if available as an alternative
- Use the scraper responsibly and ethically

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**:
   - Install ChromeDriver and add it to your PATH
   - Or specify the path: `webdriver.Chrome('/path/to/chromedriver')`

2. **Products not loading**:
   - Check if the CSS selectors match the website's HTML
   - Increase wait times if the site is slow
   - Verify the category URLs are correct

3. **Infinite scroll not working**:
   - The website might have changed its structure
   - Update the scroll detection logic
   - Check browser console for JavaScript errors

### Debug Mode

Enable debug logging to see detailed information:

```python
logging.getLogger().setLevel(logging.DEBUG)
```

## Contributing

Feel free to improve the scraper by:
- Adding support for more websites
- Improving error handling
- Optimizing performance
- Adding new features

## License

This project is for educational purposes. Make sure to comply with the target website's terms of service and applicable laws.
