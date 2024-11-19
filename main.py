import csv
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(
    filename='price_tracker.log',  # Log file name
    level=logging.INFO,            # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Here is the product URL and price threshold
product_url = "https://www.myntra.com/watches/casio/casio-men-g-shock-ga-2100-1a1dr-black-analog-digital-dial-black-resin-strap-watch-g987/10761810/buy"
price_threshold = 7000 # Price limit set to ₹7000 for the product
csv_file = "myntra.csv"  # File where we can log our scraped data

# Set up Chrome options
options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")  # Random user-agent to access the product page
options.add_argument("--headless=new")  # Run in headless mode (important for GitHub automation)
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver
#driver_path = ChromeDriverManager(version="131.0.6778.69").install()  # Automatically downloads and sets up the ChromeDriver

# Ensure header is written only if the file is empty (it defines the columns for the scraped data)
def ensure_header():
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        if file.tell() == 0:  # Add header only if the file is empty
            csv.writer(file).writerow(["Product Name", "Price", "Date"])  # Adds column headers after confirming file is empty

ensure_header()

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
 # Initializes the Chrome WebDriver with specified options

try:
    driver.get(product_url)

    # Wait for 20 seconds to allow the elements (product and price) to appear
    wait = WebDriverWait(driver, 20)
    product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-title"))).text  # Extracted product name
    price = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))).text.replace("₹", "").replace(",", "").strip())  # Extracted price
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.info(f"Extracted: {product_name}, ₹{price}, {current_date}")

    # Check if the price is below the threshold
    if price < price_threshold:
        logging.info(f"Price alert! {product_name} is now ₹{price}.")
    
    # Write product details or scraped data to CSV
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([product_name, price, current_date])
        logging.info(f"Logged to CSV: {product_name}, ₹{price}, {current_date}")

except Exception as e:
    logging.error(f"Error: {e}")

finally:
    # Quit the WebDriver
    driver.quit()
