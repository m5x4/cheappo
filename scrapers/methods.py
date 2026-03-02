

from ast import Dict

import json
import os
from datetime import datetime
from typing import List

def load_seen_products(DATA_FILE) -> Dict:
    """Load previously seen products from JSON file."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                # Migrate old format (list of IDs) to new format (dict with discounts)
                if "seen_ids" in data and isinstance(data["seen_ids"], list):
                    data["seen_products"] = {id: 0 for id in data["seen_ids"]}
                    del data["seen_ids"]
                # delete old last_updated if exists
                return data
        except (json.JSONDecodeError, IOError):
            pass
    # return {"seen_products": {}, "last_updated": None}
    return {"seen_products": {}, "last_updated": None}


def save_seen_products(seen_data: Dict, DATA_FILE: str):
    """Save seen products to JSON file."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    seen_data["last_updated"] = datetime.now().isoformat()
    with open(DATA_FILE, "w") as f:
        json.dump(seen_data, f, indent=2)


def find_new_or_better_products(current_items: List[Dict], seen_data: Dict) -> List[Dict]:
    """
    Find products that are either:
    1. New (not seen before)
    2. Have a better discount than last seen
    """
    seen_products = seen_data.get("seen_products", {})
    results = []
    
    for item in current_items:
        product_id = item["id"]
        current_discount = item["discount_percent"]
        
        if product_id not in seen_products:
            # New product
            item["is_new"] = True
            item["discount_increased"] = False
            results.append(item)
        elif current_discount > seen_products[product_id]:
            # Discount increased
            item["is_new"] = False
            item["discount_increased"] = True
            item["previous_discount"] = seen_products[product_id]
            results.append(item)
    
    return results

