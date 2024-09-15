from ui.mainUI import MainUI
from scraper.atomyScraperController import update_category, update_images, update_products
from scraper.atomyImageScraper import ImageScraper

if(__name__ == "__main__"):
  # ui = MainUI()
  # update_images()
  update_products()
  # update_category()