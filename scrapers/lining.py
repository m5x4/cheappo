"""
Li-Ning Badminton Equipment Scraper
Scrapes badminton shoes and racquets on sale with ≥10% discount from Li-Ning Singapore
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict
from .methods import load_seen_products, save_seen_products, find_new_or_better_products

# Constants
BASE_URL = "https://sg.lining.studio/collections/badminton-racket"
PRODUCTS_URL = f"{BASE_URL}/products.json"
DATA_FILE = "data/lining_data.json"
MIN_DISCOUNT_PERCENT = 20  # Only show products with >=20% discount
MIN_ORIGINAL_PRICE = 150  # Only consider products with original price >= $150


def fetch_all_products() -> List[Dict]:
    """
    Fetch all products from Li-Ning.
    Handles pagination (Shopify limits to 250 products per request).
    """
    all_products = []
    page = 1
    limit = 250  # Max allowed by Shopify
    
    while True:
        url = f"{PRODUCTS_URL}?limit={limit}&page={page}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])
            
            if not products:
                break
                
            all_products.extend(products)
            page += 1
            
            # If we got less than limit, we've reached the end
            if len(products) < limit:
                break
                
        except requests.RequestException as e:
            print(f"Error fetching products: {e}")
            break
    
    return all_products


def calculate_discount(original_price: str, sale_price: str) -> float:
    """Calculate discount percentage from prices."""
    try:
        original = float(original_price)
        sale = float(sale_price)
        if original > 0:
            return round((1 - sale / original) * 100, 1)
    except (ValueError, TypeError):
        pass
    return 0.0


def extract_product_data(products: List[Dict]) -> List[Dict]:
    """
    Extract relevant product data and filter by discount percentage.
    Returns list of products with >=10% discount.
    """
    items = []
    
    for product in products:
        product_id = str(product.get("id"))
        title = product.get("title", "Unknown")
        handle = product.get("handle", "")
        product_url = f"{BASE_URL}/products/{handle}"
        product_type = product.get("product_type", "")
        
        # Get first image
        images = product.get("images", [])
        image_url = images[0].get("src") if images else None
        
        # Get variants and find best discount
        variants = product.get("variants", [])
        
        best_discount = 0
        best_variant_data = None
        any_available = False
        
        for variant in variants:
            sale_price = variant.get("price")
            original_price = variant.get("compare_at_price")
            
            # Skip if no compare_at_price (not on sale)
            if not original_price:
                continue
            
            # Skip if original price is below minimum threshold
            if float(original_price) < MIN_ORIGINAL_PRICE:
                continue
            
            discount = calculate_discount(original_price, sale_price)
            
            # Track if any variant is available
            if variant.get("available", False):
                any_available = True
            
            # Keep track of best discount
            if discount >= MIN_DISCOUNT_PERCENT and discount > best_discount:
                best_discount = discount
                best_variant_data = {
                    "original_price": original_price,
                    "sale_price": sale_price,
                    "discount": discount
                }
        
        # Only add if we found a valid variant with good discount
        if best_variant_data:
            item = {
                "id": product_id,  # Use product_id only (not variant)
                "product_id": product_id,
                "title": title,
                "type": product_type,  # "Badminton Shoes", "Badminton Racket", etc.
                "original_price": f"${best_variant_data['original_price']}",
                "sale_price": f"${best_variant_data['sale_price']}",
                "discount_percent": best_variant_data['discount'],
                "available": any_available,
                "url": product_url,
                "image_url": image_url,
                "scraped_at": datetime.now().isoformat()
            }
            items.append(item)
    
    # Sort by discount percentage (highest first)
    items.sort(key=lambda x: x["discount_percent"], reverse=True)
    
    return items

def scrape_sale_products(min_discount: float = MIN_DISCOUNT_PERCENT) -> List[Dict]:
    """
    Main scraping function.
    Returns list of products on sale with discount >= min_discount.
    """
    print(f"Fetching sale products from Li-Ning...")
    products = fetch_all_products()
    print(f"Found {len(products)} products total")
    
    items = extract_product_data(products)
    print(f"Found {len(items)} products with >={min_discount}% discount")
    
    return items


def format_product_message(item: Dict) -> str:
    """Format a product into a Telegram message."""
    availability = "✅ In Stock" if item["available"] else "❌ Out of Stock"
    
    # Add emoji based on product type
    emoji = "🏸"
    if "shoe" in item["type"].lower():
        emoji = "👟"
    elif "racket" in item["type"].lower() or "racquet" in item["type"].lower():
        emoji = "🏸"
    elif "string" in item["type"].lower():
        emoji = "🎾"
    
    # Check if this is a discount increase
    if item.get("discount_increased"):
        previous = item.get("previous_discount", 0)
        discount_line = f"📉 Discount: *{item['discount_percent']}% OFF!* (was {previous}%)"
        header = "🔥 *PRICE DROP!*\n\n"
    else:
        discount_line = f"📉 Discount: *{item['discount_percent']}% OFF!*"
        header = ""
    
    message = (
        f"{header}"
        f"{emoji} *{item['title']}*\n"
        f"📦 Type: {item['type']}\n"
        f"💰 Original: ~~{item['original_price']}~~\n"
        f"🔥 Sale: *{item['sale_price']}*\n"
        f"{discount_line}\n"
        f"{availability}\n"
        f"🛒 [Buy Now]({item['url']})"
    )
    return message


def get_new_sale_products() -> List[Dict]:
    """
    Scrape and return NEW products or ones with INCREASED discount.
    Updates the seen products file.
    """
    # Scrape current products
    current_items = scrape_sale_products()
    
    # Load seen products
    seen_data = load_seen_products(DATA_FILE)
    
    # Find new products or ones with better discounts
    notable_items = find_new_or_better_products(current_items, seen_data)
    
    # Update seen products with current IDs and discounts
    seen_data["seen_products"] = {
        i["id"]: i["discount_percent"] for i in current_items
    }
    save_seen_products(seen_data, DATA_FILE)
    
    new_count = sum(1 for i in notable_items if i.get("is_new", False))
    increased_count = sum(1 for i in notable_items if i.get("discount_increased", False))
    print(f"Found {new_count} NEW products and {increased_count} with increased discounts!")
    
    return notable_items


# For testing
if __name__ == "__main__":
    print("=" * 60)
    print("Li-Ning Badminton Equipment Sale Scraper")
    print("=" * 60)
    
    items = scrape_sale_products()
    
    print(f"\n{'=' * 60}")
    print(f"PRODUCTS WITH >={MIN_DISCOUNT_PERCENT}% DISCOUNT:")
    print("=" * 60)
    
    for i, item in enumerate(items[:10], 1):  # Show top 10
        print(f"\n{i}. {item['title']}")
        print(f"   Type: {item['type']}")
        print(f"   Original: {item['original_price']} → Sale: {item['sale_price']}")
        print(f"   Discount: {item['discount_percent']}% OFF")
        print(f"   Available: {'Yes' if item['available'] else 'No'}")
        print(f"   URL: {item['url']}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {len(items)} products with >={MIN_DISCOUNT_PERCENT}% discount")
    print("=" * 60)