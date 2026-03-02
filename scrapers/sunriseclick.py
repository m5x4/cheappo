"""
SunriseClick Badminton Racquet Scraper
Scrapes racquets on sale with ≥10% discount from SunriseClick Singapore
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict
from .methods import load_seen_products, save_seen_products, find_new_or_better_products


# Constants
BASE_URL = "https://sg.sunriseclick.com"
COLLECTION_URL = f"{BASE_URL}/collections/sale-badminton-racquets/products.json"
DATA_FILE = "data/racquet_data.json"
MIN_DISCOUNT_PERCENT = 20  # Only show racquets with >=20% discount
MIN_ORIGINAL_PRICE = 200  # Only consider racquets with original price >= $200


def fetch_all_products() -> List[Dict]:
    """
    Fetch all products from the sale-badminton-racquets collection.
    Handles pagination (Shopify limits to 250 products per request).
    """
    all_products = []
    page = 1
    limit = 250  # Max allowed by Shopify
    
    while True:
        url = f"{COLLECTION_URL}?limit={limit}&page={page}"
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


def extract_racquet_data(products: List[Dict]) -> List[Dict]:
    """
    Extract relevant racquet data and filter by discount percentage.
    Returns list of racquets (one per model/title) with >=10% discount.
    Uses the best discount available across all variants.
    """
    racquets = []
    
    for product in products:
        product_id = str(product.get("id"))
        title = product.get("title", "Unknown")
        handle = product.get("handle", "")
        product_url = f"{BASE_URL}/products/{handle}"
        
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
            racquet = {
                "id": product_id,  # Use product_id only (not variant)
                "product_id": product_id,
                "title": title,
                "original_price": f"${best_variant_data['original_price']}",
                "sale_price": f"${best_variant_data['sale_price']}",
                "discount_percent": best_variant_data['discount'],
                "available": any_available,
                "url": product_url,
                "image_url": image_url,
                "scraped_at": datetime.now().isoformat()
            }
            racquets.append(racquet)
    
    # Sort by discount percentage (highest first)
    racquets.sort(key=lambda x: x["discount_percent"], reverse=True)
    
    return racquets


def format_racquet_message(racquet: Dict) -> str:
    """Format a racquet into a Telegram message."""
    availability = "✅ In Stock" if racquet["available"] else "❌ Out of Stock"
    
    # Check if this is a discount increase
    if racquet.get("discount_increased"):
        previous = racquet.get("previous_discount", 0)
        discount_line = f"📉 Discount: *{racquet['discount_percent']}% OFF!* (was {previous}%)"
        header = "🔥 *PRICE DROP!*\n\n"
    else:
        discount_line = f"📉 Discount: *{racquet['discount_percent']}% OFF!*"
        header = ""
    
    message = (
        f"{header}"
        f"🏸 *{racquet['title']}*\n"
        f"💰 Original: ~~{racquet['original_price']}~~\n"
        f"🔥 Sale: *{racquet['sale_price']}*\n"
        f"{discount_line}\n"
        f"{availability}\n"
        f"🛒 [Buy Now]({racquet['url']})"
    )
    return message


def scrape_sale_racquets(min_discount: float = MIN_DISCOUNT_PERCENT) -> List[Dict]:
    """
    Main scraping function.
    Returns list of racquets on sale with discount >= min_discount.
    """
    print(f"Fetching sale racquets from SunriseClick...")
    products = fetch_all_products()
    print(f"Found {len(products)} products in sale collection")
    
    racquets = extract_racquet_data(products)
    print(f"Found {len(racquets)} racquet variants with >={min_discount}% discount")
    
    return racquets


def get_new_sale_racquets() -> List[Dict]:
    """
    Scrape and return NEW racquets or ones with INCREASED discount.
    Updates the seen products file.
    """
    # Scrape current racquets
    current_racquets = scrape_sale_racquets()
    
    # Load seen products
    seen_data = load_seen_products(DATA_FILE)
    
    # Find new racquets or ones with better discounts
    notable_racquets = find_new_or_better_products(current_racquets, seen_data)
    
    # Update seen products with current IDs and discounts
    seen_data["seen_products"] = {
        r["id"]: r["discount_percent"] for r in current_racquets
    }
    save_seen_products(seen_data, DATA_FILE)
    
    new_count = sum(1 for r in notable_racquets if r.get("is_new", False))
    increased_count = sum(1 for r in notable_racquets if r.get("discount_increased", False))
    print(f"Found {new_count} NEW racquets and {increased_count} with increased discounts!")
    
    return notable_racquets


# For testing
if __name__ == "__main__":
    print("=" * 60)
    print("SunriseClick Badminton Racquet Sale Scraper")
    print("=" * 60)
    
    racquets = scrape_sale_racquets()
    
    print(f"\n{'=' * 60}")
    print(f"RACQUETS WITH >={MIN_DISCOUNT_PERCENT}% DISCOUNT:")
    print("=" * 60)
    
    for i, racquet in enumerate(racquets[:10], 1):  # Show top 10
        print(f"\n{i}. {racquet['title']}")
        print(f"   Variant: {racquet['variant']}")
        print(f"   Original: {racquet['original_price']} → Sale: {racquet['sale_price']}")
        print(f"   Discount: {racquet['discount_percent']}% OFF")
        print(f"   Available: {'Yes' if racquet['available'] else 'No'}")
        print(f"   URL: {racquet['url']}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {len(racquets)} racquet variants with >={MIN_DISCOUNT_PERCENT}% discount")
    print("=" * 60)
