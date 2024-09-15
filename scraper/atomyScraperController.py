from scraper.atomyCategoryScraper import AtomyCategoryScraper
from scraper.atomyProductsScraper import AtomyProductsScraper
from PyQt6 import QtWidgets
from pprint import pprint

def update_category():
  scraper = AtomyCategoryScraper()
  scraper.get_LM_category()
  scraper.get_SClass_titles()
  scraper.transform_to_json()
  pprint(scraper.allCategory)
  print("Scraped Done!")

def update_products():
  products_scraper = AtomyProductsScraper()
  products_scraper.add_hemohim()
  products_scraper.scrape()
  products_scraper.transform_to_json()

  print("Update Products Success!")

def update_images():
  pass