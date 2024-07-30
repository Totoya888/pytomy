from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json
from pprint import pprint

from bs4 import BeautifulSoup
import requests

class AtomyProductsScraper:
  def __init__(self, progress_bar):
    self.driver = webdriver.Edge()
    self.LClass = "02"
    self.MClass = "01"
    self.SClass = "01"
    self.all_products = {"body": []}
    self.URL = 'https://www.atomy.com:449/tw/Home/Product/ProductList'
    
  def select_all(self):
    select = Select(self.driver.find_element(By.ID, 'CountPerPage'))
    select.select_by_value('1000')

  def get_data(self):
    return self.all_products

  def scrape(self):
    self.driver.get(self.URL + f'?LClass={self.LClass}&MClass={self.MClass}&SClass={self.SClass}')
    self.select_all()
    jsonFile = open('db/atomy_category.json', 'r', encoding='utf-8')
    r = jsonFile.read()
    json_data = json.loads(r)

    for L in json_data['category'][1:-1]:
      print("L index: ", L['index'])
      self.all_products['body'].append({
        "LClass": L['index'],
        "sub": []
      })
      for M in L['subCategories']:
        self.all_products['body'][-1]['sub'].append({
          "MClass": M['index'],
          "sub": []
        })
        if len(M['items']) == 0:
          SClass = "00"
          cur_url = self.URL + f'?LClass={L['index']}&MClass={M["index"]}&SClass={SClass}'
          box_info = self.get_box_info(cur_url)
          li = self.box_info_to_list(box_info)
          self.all_products['body'][-1]['sub'][-1]['sub'].append({
            "SClass": SClass,
            "infos": li
          })
        else:
          for S in M['items']:
            cur_url = self.URL + f'?LClass={L['index']}&MClass={M["index"]}&SClass={S["index"]}'
            box_info = self.get_box_info(cur_url)
            li = self.box_info_to_list(box_info)
            self.all_products['body'][-1]['sub'][-1]['sub'].append({
              "SClass": S['index'],
              "infos": li
            })
            # print("Box Info: ", box_info)


  def get_box_info(self, url):
    self.driver.get(url)
    self.select_all()

    ptitles = self.driver.find_elements(By.CLASS_NAME, 'ptitle')
    titles = [i.text for i in ptitles if i.text != '']

    pprices = self.driver.find_elements(By.CLASS_NAME, 'pprice')
    prices = [i.find_element(By.TAG_NAME, 'span').text for i in pprices if i.text != '']

    ppoints = self.driver.find_elements(By.CLASS_NAME, 'ppoint')
    points = [i.find_element(By.TAG_NAME, 'span').text for i in ppoints if i.text != '']

    # print(len(prices), len(points), len(titles))
    return {
      "titles": titles,
      "prices": prices,
      "points": points,
      "length": len(titles)
    }
  
  def box_info_to_list(self, box_info):
    data = []
    for i in range(box_info['length']):
      data.append({
        "title": box_info['titles'][i],
        "price": box_info['prices'][i],
        "point": box_info['points'][i]
      })
    return data

  def transform_to_json(self):
    jsonFile = open('db/atomy_products.json', 'w', encoding='utf-8')
    json.dump(self.all_products, jsonFile, ensure_ascii=False, indent=4)

  def add_hemohim(self):
    url = 'https://www.atomy.com:449/tw/Home/Product/ProductList?LClass=01'
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'html.parser')

    proList = soup.find('div', class_='proList')

    li_titles = proList.find_all('li', class_='ptitle')
    titles = [i.find('a').get_text() for i in li_titles]
    
    li_prices = proList.find_all('li', class_='pprice')
    prices = [i.find('strong').get_text() for i in li_prices]

    li_points = proList.find_all('li', class_='ppoint')
    points = [i.find('strong').get_text() for i in li_points]

    self.all_products['body'].append({
      "LClass": "01",
      "infos": []
    })

    for i in range(len(titles)):
      self.all_products['body'][-1]['items'].append({
        "title": titles[i],
        "price": prices[i],
        "point": points[i]
      })