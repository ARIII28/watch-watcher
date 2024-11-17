import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

# Constants
product_url = "https://www.myntra.com/watches/casio/casio-men-g-shock-ga-2100-1a1dr-black-analog-digital-dial-black-resin-strap-watch-g987/10761810/buy"
price_threshold = 6500  # Set the price limit
csv_file = "myntra.csv"

# Set up Chrome options
options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues in containers

# Set up ChromeDriver
service = Service(ChromeDriverManager().install())

# Ensure the CSV file has a header
def ensure_header():
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        if file.tell() == 0:  # Add header if the file is empty
            csv.writer(file).writerow(["Product Name", "Price", "Date"])

ensure_header()

# Perform the price check
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the product page
    driver.get(product_url)
    
    # Wait for elements to load and extract data
    wait = WebDriverWait(driver, 20)
    product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-title"))).text
    price = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))).text.replace("₹", "").replace(",", "").strip())
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Extracted: {product_name}, ₹{price}, {current_date}")
    
    # Check if price is below threshold
    if price < price_threshold:
        print(f"Price alert! {product_name} is now ₹{price}.")
    
    # Write data to the CSV file
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([product_name, price, current_date])
        print(f"Logged to CSV: {product_name}, ₹{price}, {current_date}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Quit the WebDriver
    driver.quit()
