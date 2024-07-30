from ui.widgets.updateData_ui import Ui_Form
from PyQt6 import QtWidgets,QtCore
import datetime
from scraper.atomyScraperController import update_category, update_products

class UpdateDataController:
  def __init__(self, category_date, products_date) -> None:
    self.updateData_window = QtWidgets.QWidget()
    self.form = Ui_Form()
    self.form.setupUi(self.updateData_window)
    x = self.updateData_window.pos().x()
    y = self.updateData_window.pos().y()
    self.updateData_window.move(x+100, y+100)

    self.category_date = category_date
    self.products_date = products_date

    self.set_timmer()
    self.form.updateCategory.clicked.connect(lambda: update_category(self.form.progressBar))
    self.form.updateProduct.clicked.connect(lambda: update_products(self.form.progressBar))

  def set_timmer(self):
    timer = QtCore.QTimer(self.updateData_window)
    timer.timeout.connect(self.get_now_date)
    timer.start(1000) 

  def get_now_date(self):
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    now_str = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    self.form.now_date.setText("目前時間: " + now_str)

  def set_data_date(self):
    self.form.categoryDate.setText("類別資料更新時間: " + self.category_date)
    self.form.productDate.setText("產品資料更新時間: " + self.products_date)