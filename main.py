import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

## here the product i've wanted to track or its webpage
product_url = "https://www.myntra.com/watches/casio/casio-men-g-shock-ga-2100-1a1dr-black-analog-digital-dial-black-resin-strap-watch-g987/10761810/buy"
price_threshold = 6500  #  so here the Price limit set to ₹6500 for the product
csv_file = "myntra.csv" #file where we can log our scraped data

# Set up Chrome options
options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}") # this is really important to generate random agent to access the product page 
options.add_argument("--headless")  # Run in headless mode its optional but for my automation process in github its important
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage") 

# Set up ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

# its download ChromeDriver corresponding to your installed Chrome version
service = Service("/usr/local/bin/chromedriver")

  # Automatically downloads and sets up the ChromeDrive

# Ensure header is written only if the file is empty (it defines the columns for the scraped data)
def ensure_header():
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        if file.tell() == 0:  # Add header only if the file is empty 
            csv.writer(file).writerow(["Product Name", "Price", "Date"])## it adds column headers after confirming file is empty

ensure_header()


driver = webdriver.Chrome(service=service, options=options) ##as we know it initialize the Chrome WebDriver with our specified options

try:
    
    driver.get(product_url)
    
    # it waits for 20 seconds to element(product and price) to appear
    wait = WebDriverWait(driver, 20)
    product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-title"))).text   #extracted the product name from the webpage.
    price = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))).text.replace("₹", "").replace(",", "").strip())###we are extracting the price as text and make it int.
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Extracted: {product_name}, ₹{price}, {current_date}")
    
    # Check if price is below threshold
    if price < price_threshold:
        print(f"Price alert! {product_name} is now {price}.")
    
    # Write product details or scraped data to CSV
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([product_name, price, current_date])
        print(f"Logged to CSV: {product_name}, {price}, {current_date}")

except Exception as e:
    print(f"Error: {e}")
    raise

finally:
    # Quit the WebDriver
    driver.quit()
    