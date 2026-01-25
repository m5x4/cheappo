"""
Shopee/Nike Scraper
Scrapes Nike sale products
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def scrape_nike_discounts():
    # currently does not work due to the website structure
    return ""
    """Scrapes Nike for discounted products"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.nike.com/w/mens-sale-shoes-3yaepznik1zy7ok"
    driver.get(url)
    time.sleep(3)

    items = []
    products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card__body')

    for product in products[:3]:
        try:
            title = product.find_element(By.CSS_SELECTOR, 'div.product-card__title').text
            original_price = product.find_element(By.CSS_SELECTOR, 'div.product-price.is--striked-out').text
            discounted_price = product.find_element(By.CSS_SELECTOR, 'div.product-price:not(.is--striked-out)').text
            discount_percentage = product.find_element(By.CSS_SELECTOR, 'div.product-price__perc.css-1rz91t').text
            link = product.find_element(By.CSS_SELECTOR, 'a.product-card__link-overlay').get_attribute('href')

            items.append({
                "title": title,
                "original_price": original_price,
                "discounted_price": discounted_price,
                "discount_percentage": discount_percentage,
                "link": link,
            })
        except Exception as e:
            print("Error scraping product:", e)

    driver.quit()
    return items
