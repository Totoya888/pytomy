# Form implementation generated from reading ui file 'c:\Darren\PythonProject\pytomy\ui\widgets\updateData.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(16)
        Form.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 29, 741, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.categoryDate = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.categoryDate.setObjectName("categoryDate")
        self.horizontalLayout.addWidget(self.categoryDate)
        self.updateCategory = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.updateCategory.setObjectName("updateCategory")
        self.horizontalLayout.addWidget(self.updateCategory)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.productDate = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.productDate.setObjectName("productDate")
        self.horizontalLayout_3.addWidget(self.productDate)
        self.updateProduct = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.updateProduct.setObjectName("updateProduct")
        self.horizontalLayout_3.addWidget(self.updateProduct)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.progressBar = QtWidgets.QProgressBar(parent=self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.textEdit = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.now_date = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.now_date.setObjectName("now_date")
        self.horizontalLayout_4.addWidget(self.now_date)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "更新資料"))
        self.categoryDate.setText(_translate("Form", "類別資料時間:2024-07-01"))
        self.updateCategory.setText(_translate("Form", "更新類別"))
        self.productDate.setText(_translate("Form", "商品資料時間:2024-07-01"))
        self.updateProduct.setText(_translate("Form", "更新商品"))
        self.now_date.setText(_translate("Form", "現在時間: "))
