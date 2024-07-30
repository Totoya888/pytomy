from scraper.atomyCategoryScraper import AtomyCategoryScraper
from scraper.atomyProductsScraper import AtomyProductsScraper
from PyQt6 import QtWidgets

def update_category(progress_bar: QtWidgets.QProgressBar):
  scraper = AtomyCategoryScraper(progress_bar)
  scraper.get_LM_category()
  scraper.get_SClass_titles()
  scraper.transform_to_json()
  print(scraper.allCategory)

def update_products(progress_bar: QtWidgets.QProgressBar):
  products_scraper = AtomyProductsScraper(progress_bar)
  products_scraper.add_hemohim()
  products_scraper.scrape()
  products_scraper.transform_to_json()  