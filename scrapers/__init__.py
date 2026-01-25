"""
Scrapers Module
All web scrapers for different sites

Import scrapers directly from their modules to avoid dependency issues:
  from scrapers.sunriseclick import scrape_sale_racquets
  from scrapers.shopee import scrape_nike_discounts
"""

# Don't auto-import to avoid requiring all dependencies (e.g., selenium)
__all__ = [
    'scrape_nike_discounts',
    'scrape_sale_racquets',
    'get_new_sale_racquets',
]
