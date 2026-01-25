from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in the background (optional)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Nike's website
url = "https://www.nike.com/w/mens-shoes-nik1zy7ok"
driver.get(url)

# Let the page load
time.sleep(3)

# Extract product names and prices
products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__body')

for product in products:
    try:
        title = product.find_element(By.CSS_SELECTOR, 'div.product-card__title').text
        price = product.find_element(By.CSS_SELECTOR, 'div.product-price').text
        print(f"{title} - {price}")
    except:
        pass

# Close the driver
driver.quit()
