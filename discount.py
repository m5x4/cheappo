from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs without opening a browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Nike's website (Men's Shoes)
# url = "https://www.nike.com/w/mens-shoes-nik1zy7ok"
url = "https://www.nike.com/sg/w/seasonal-sale-lt4x"
driver.get(url)

# Let the page load fully
time.sleep(3)

# Find all product cards
products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__body')

# Loop through products and filter discounted items
print("running...")
count = 0
for product in products:
    count+=1
    if count > 5:
        break
    try:
        title = product.find_element(By.CSS_SELECTOR, 'div.product-card__title').text
        original_price = product.find_element(By.CSS_SELECTOR, 'div.product-price.is--striked-out').text
        discounted_price = product.find_element(By.CSS_SELECTOR, 'div.product-price:not(.is--striked-out)').text

        print(f"🔥 {title} - Original: {original_price}, Discounted: {discounted_price}")
    except:
        # Skip items without discounts
        pass

for _ in range(3):  # Scroll multiple times to load more items
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Close the driver
driver.quit()
