from PyQt6 import QtWidgets,QtCore
import sys
from ui.beta01_ui import Ui_MainWindow
import json
from pprint import pprint
from ui.widgets.updateDataController import UpdateDataController

class MainUI:
  def __init__(self) -> None:
    self.app = QtWidgets.QApplication(sys.argv)
    self.MainWindow = QtWidgets.QMainWindow()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self.MainWindow)
    # self.MainWindow.show()
    category_file = open("./db/atomy_category.json", "r", encoding="utf-8")
    self.category = json.load(category_file)
    products_file = open("./db/atomy_products.json", "r", encoding="utf-8")
    self.products = json.load(products_file)
    self.ui.actionUpdate.triggered.connect(self.open_updateData_window)
    self.open_updateData_window() # for test

    self.L_index = 0
    self.M_index = 0
    self.S_index = 0

    self.init_category()
    data = self.list_2d_to_1d(self.collect_all_L_products())
    self.update_table(data)

    sys.exit(self.app.exec())

  def init_category(self):
    self.ui.LClass.addItem("全部")
    self.ui.MClass.addItem("全部")
    self.ui.SClass.addItem("全部")
    self.ui.MClass.setDisabled(True)
    self.ui.SClass.setDisabled(True)

    for i in self.category['category']:
      self.ui.LClass.addItems([i['name']])

    self.ui.LClass.activated.connect(self.set_M_items)
    self.ui.MClass.activated.connect(self.set_S_items)
    self.ui.SClass.activated.connect(self.update_products)

  def set_M_items(self, index):
    if index == 0:
      self.ui.MClass.clear()
      self.ui.SClass.clear()
      self.ui.MClass.addItem("全部")
      self.ui.SClass.addItem("全部")
      self.ui.MClass.setDisabled(True)
      self.ui.SClass.setDisabled(True)
      self.L_index = 0
      self.M_index = 0
      self.S_index = 0
    else:
      if index == 1:
        self.process_hemohim()
        return
      self.L_index = index
      self.M_index = 0
      self.S_index = 0
      self.ui.MClass.setDisabled(False)
      self.ui.SClass.setDisabled(False) 
      self.ui.MClass.clear()
      self.ui.SClass.clear()
      self.ui.MClass.addItem("全部")
      self.ui.SClass.addItem("全部")
      li = [i['name'] for i in self.category['category'][index-1]['subCategories'] if i is not None]
      self.ui.MClass.addItems(li)

    self.update_products()

  def set_S_items(self, index):
    if index == 0:
      self.M_index = 0
      self.S_index = 0
      self.ui.SClass.clear()
      self.ui.SClass.addItem("全部")
      self.ui.SClass.setDisabled(True)
    else:
      self.M_index = index
      self.S_index = 0
      self.ui.SClass.setDisabled(False)
      self.ui.SClass.clear()
      self.ui.SClass.addItem("全部")
      
      self.L_index = self.ui.LClass.currentIndex()
      li = [i['name'] for i in self.category['category'][self.L_index-1]['subCategories'][index-1]['items'] if i is not None]
      self.ui.SClass.addItems(li)

    self.update_products()
  
  def get_selected_index(self):
    self.L_index = self.ui.LClass.currentIndex()
    self.M_index = self.ui.MClass.currentIndex()
    self.S_index = self.ui.SClass.currentIndex()
    print("Current index: ", self.L_index, self.M_index, self.S_index)
    return self.L_index, self.M_index, self.S_index
  
  def update_products(self, index=None):
    index = self.get_selected_index()
    data = []
    if index[0] == 0: #Show all
      data = self.collect_all_L_products()
    else:
      if index[1] == 0:
        data = self.collect_all_M_products(index[0])
      else:
        if index[2] == 0:
          data = self.collect_all_S_products(index[0], index[1])
        else:
          data = self.collect_selected_products()
          self.update_table(data)
          return
    data = self.list_2d_to_1d(data)
    self.update_table(data)

  def collect_all_L_products(self):
    data = []
    data.append(self.products['body'][0]['infos'])
    for L in self.products['body'][1:-1]:
        for M in L['sub']:
          for S in M['sub']:
            data.append(S['infos'])
    return data
  
  def collect_all_M_products(self, L_index):
    data = []
    if L_index == 1: return
    for M in self.products['body'][L_index-1]['sub']:
      for S in M['sub']:
        data.append(S['infos'])
    return data
  
  def collect_all_S_products(self, L_index, M_index):
    data = []
    if L_index == 1: return
    for S in self.products['body'][L_index-1]['sub'][M_index-1]['sub']:
      data.append(S['infos'])
    return data
  
  def collect_selected_products(self):
    L_index, M_index, S_index = self.get_selected_index()
    if L_index == 1: return
    data = self.products['body'][L_index-1]['sub'][M_index-1]['sub'][S_index-1]['infos']
    return data
  
  def list_2d_to_1d(self, list_2d):
    return [item for sublist in list_2d for item in sublist]
  
  def remove_comma(self, string):
    return int(string.replace(',', ''))
  
  def update_table(self, data: list):
    from utils.identify_multi_item import identify_multi_item
    self.ui.tableWidget.setSortingEnabled(False)
    self.ui.tableWidget.verticalHeader().setVisible(False)
    self.ui.tableWidget.setRowCount(len(data))
    for index, item in enumerate(data):
      self.ui.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 0).setData(QtCore.Qt.ItemDataRole.DisplayRole, int(str(index+1)))

      title = item['title']
      quantity, text = identify_multi_item(title)
      # if quantity > 1:
      #   print(index, title, text)
      self.ui.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(title))

      price = self.remove_comma(item['price'])
      self.ui.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 2).setData(QtCore.Qt.ItemDataRole.DisplayRole, price)

      self.ui.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 3).setData(QtCore.Qt.ItemDataRole.DisplayRole, float(price / quantity))

      point = self.remove_comma(item['point'])
      self.ui.tableWidget.setItem(index, 4, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 4).setData(QtCore.Qt.ItemDataRole.DisplayRole, point)

      self.ui.tableWidget.setItem(index, 5, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 5).setData(QtCore.Qt.ItemDataRole.DisplayRole, float(point / quantity))

      self.ui.tableWidget.setItem(index, 6, QtWidgets.QTableWidgetItem())
      self.ui.tableWidget.item(index, 6).setData(QtCore.Qt.ItemDataRole.DisplayRole, float(point / price))

      self.ui.tableWidget.setItem(index, 7, QtWidgets.QTableWidgetItem(text))
    
    self.ui.tableWidget.setColumnWidth(0, 50)
    self.ui.tableWidget.setColumnWidth(1, 260)
    self.ui.tableWidget.setColumnWidth(7, 300)
    self.ui.tableWidget.setSortingEnabled(True)
    self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
    self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

  def process_hemohim(self):
    self.L_index = 1
    self.M_index = 0
    self.S_index = 0
    self.ui.MClass.setDisabled(True)
    self.ui.SClass.setDisabled(True) 
    self.ui.MClass.clear()
    self.ui.SClass.clear()
    self.ui.MClass.addItem("全部")
    self.ui.SClass.addItem("全部")
    data = self.products['body'][0]['infos']
    self.update_table(data)

  def open_updateData_window(self):
    self.updateData_controller = UpdateDataController()
    self.updateData_controller.updateData_window.show()