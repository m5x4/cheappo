"""
Scrapers Module
All web scrapers for different sites
"""

from scrapers.shopee import scrape_nike_discounts
from scrapers.sunriseclick import scrape_sale_racquets, get_new_sale_racquets

__all__ = [
    'scrape_nike_discounts',
    'scrape_sale_racquets',
    'get_new_sale_racquets',
]
