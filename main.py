import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
   
   
# here the product i've wanted to track or its webpage
product_url = "https://www.myntra.com/watches/casio/casio-men-g-shock-ga-2100-1a1dr-black-analog-digital-dial-black-resin-strap-watch-g987/10761810/buy"
price_threshold = 6500 #  so here the Price limit set to ₹6500 for the product
csv_file = "myntra.csv"
chrome_driver = ChromeDriverManager().install() # Location for ChromeDriver in GitHub Actions
  # Download ChromeDriver; if you are using Brave, specify the binary path for the WebDriver


# set Chrome options and set a dynamic user-agent to mimic real user behavior

options = Options()
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}") 

options.add_argument("--headless")# entirely optional
options.add_argument("--disable-gpu")
options.add_argument("--disable-popup-blocking")  # Disable popups
options.add_argument("--disable-notifications")  # Disable notifications
options.add_argument("--disable-infobars") 

# Set up Service
service = Service(chrome_driver) 

# Ensure header is written only if the file is empty (it defines the columns for the scraped data)
def ensure_header():
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:  
        if file.tell() == 0: # Checking if the file is empty before adding header 
            csv.writer(file).writerow(["Product Name", "Price", "Date"]) # it adds column headers after confirming file is empty



ensure_header()





while True: #it creates an infinite loop to track the price
    driver = webdriver.Chrome(service=service, options=options)  #as we know it initialize the Chrome WebDriver with our specified options
    
    try:
        driver.get(product_url)
        wait = WebDriverWait(driver, 20)  # Make the driver wait for up to 20 seconds for the page to load
        product_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.pdp-title"))).text #extracted the product name from the webpage and chnaging
        price = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "strong"))).text.replace("₹", "").replace(",", "").strip()) #we are extracting the price as text and make it int.
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    
        print(f"Extracted: {product_name}, ₹{price}, {current_date}")

        # Check if price is below threshold
        if price < price_threshold:
            print(f"Price alert! {product_name} is now ₹{price}.")

        # Write product details to CSV
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow([product_name, price, current_date])
            print(f"Logged to CSV: {product_name}, ₹{price}, {current_date}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the browser
        driver.quit()

    # Wait for 86400 seconds (24 hours) before checking again
    time.sleep(86400)


