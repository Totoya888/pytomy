from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time
import pprint
import re
import json
from PyQt6 import QtWidgets
from datetime import datetime

class AtomyCategoryScraper:
  def __init__(self) -> None:
    self.LClass = '02'
    self.MClass = '01'
    self.SClass = '00'
    self.allCategory = {"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"category": []}
    self.URL = 'https://www.atomy.com:449/tw/Home/Product/ProductList'
    # self.driver = webdriver.Edge()
    self.progress_value = 0

  def select_all(self):
    time.sleep(0.5)
    select = Select(self.driver.find_element(By.ID, 'CountPerPage'))
    select.select_by_value('1000')

  def turn_page(self, L):
     self.driver.get(self.URL+f"?LClass={L}")

  def get_title(self) -> str:
    pass

  def filter_string(self, string):
     if '\n' in string:
        return False
     else: 
        return True
  
  def get_LM_category(self):
    for i in range(1, 9):
      self.LClass = "0" + str(i)
      self.MClass = "01"
      self.SClass = "01"
      web = requests.get(self.URL+f"?LClass={self.LClass}")
      soup = BeautifulSoup(web.text, 'html5lib')
      Ltitle = soup.find('h2').get_text()
      self.allCategory['category'].append({"index": self.LClass, "name": Ltitle, "subCategories": []})      
      
      # get MClass titles
      Mpattern = re.compile(r'00$')
      Mtitles = soup.find_all('a', href=Mpattern)
      for Mtitle in Mtitles:
        Mtitle_text = Mtitle.get_text()
        if self.filter_string(Mtitle_text):
          self.allCategory['category'][-1]['subCategories'].append({"index": self.MClass, "name": Mtitle_text, "items": []})
        else:
          self.allCategory['category'][-1]['subCategories'].append({"index": self.MClass, "name": "Some problem?!", "items": []})
        if int(self.MClass) < 9:
          self.MClass =  "0" + str(int(self.MClass) + 1)
        else:
          self.MClass = str(int(self.MClass) + 1)

  def get_SClass_titles(self):
      for i in range(2, 9):
        self.LClass = "0" + str(i)
        self.MClass = "01"
        self.SClass = "01"
        web = requests.get(self.URL + f"?LClass={self.LClass}")
        soup = BeautifulSoup(web.text, 'html5lib')
        Spattern = re.compile(r'ProductList\?LClass=\d{2}&MClass=\d{2}&SClass=(?!00)\d{2}')
        Stitles = soup.find('ul', class_='pSubMenu').findChildren('a', href=Spattern)
        for Stitle in Stitles:
          url = Stitle['href']
          pattern = re.compile(r'LClass=(\d+)&MClass=(\d+)&SClass=(\d+)')
          # 匹配並提取值
          match = pattern.search(url)
          if match:
              lclass_value = match.group(1)
              mclass_value = match.group(2)
              sclass_value = match.group(3)
              self.allCategory['category'][int(lclass_value) - 1]['subCategories'][int(mclass_value) - 1]['items'].append({"index": sclass_value, "name": Stitle.get_text()})
          else:
              print("匹配失敗")
      
  def transform_to_json(self):
    jsonFile = open('./db/atomy_category.json', 'w', encoding='utf-8')
    json.dump(self.allCategory, jsonFile, indent=4, ensure_ascii=False)  

  
  def get_merchandises(self): # TODO: Have to improve.
    self.LClass = "02"
    self.MClass = "01"
    self.SClass = "01"
    web = requests.get(self.URL+f"?LClass={self.LClass}")
    soup = BeautifulSoup(web.text, 'html.parser')
    titles = soup.find_all('li', class_='ptitle')
    print(titles)