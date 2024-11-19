import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import os

# Product and price threshold settings
product_url = "https://www.myntra.com/watches/casio/casio-men-g-shock-ga-2100-1a1dr-black-analog-digital-dial-black-resin-strap-watch-g987/10761810/buy"
price_threshold = 6500  # Price limit set to ₹6500 for the product
csv_file = "myntra.csv"  # File where we can log our scraped data

# Set up Chrome options
options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")  # Random user-agent for access
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

# Set up ChromeDriver
if os.environ.get("GITHUB_ACTIONS") is None:  # Running locally (not in GitHub Actions)
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())  # Automatically download and set up ChromeDriver
else:  # Running in GitHub Actions
    service = Service("/usr/local/bin/chromedriver")  # Use the pre-installed ChromeDriver in GitHub Actions

# Ensure header is written only if the file is empty (it defines the columns for the scraped data)
def ensure_header():
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        if file.tell() == 0:  # Add header only if the file is empty 
            csv.writer(file).writerow(["Product Name", "Price", "Date"])

ensure_header()

# Initialize WebDriver with ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(product_url)
    
    # Wait for elements to appear (product name and price)
    wait = WebDriverWait(driver, 20)
    product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-title"))).text
    price = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))).text.replace("₹", "").replace(",", "").strip())
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Extracted: {product_name}, ₹{price}, {current_date}")
    
    # Check if price is below threshold
    if price < price_threshold:
        print(f"Price alert! {product_name} is now {price}.")
    
    # Write product details to CSV
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([product_name, price, current_date])
        print(f"Logged to CSV: {product_name}, {price}, {current_date}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Quit the WebDriver
    driver.quit()
