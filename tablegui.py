import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
import time


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Table Editor'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()



        def check_fun(decision):
            qwidget = QWidget()
            checkbox = QCheckBox()
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.setAlignment(Qt.AlignCenter)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setContentsMargins(0, 0, 0, 0)
            checkbox.setChecked(decision)
            return qwidget

        def add_meal():
            self.tableWidget.insertRow(0)
            self.tableWidget.setCellWidget(0, 0, check_fun(True))
            self.tableWidget.setCellWidget(0, 2, check_fun(False))
            save_text.setHidden(True)

        def save_table():
            active = []
            Vegetarian = []
            Dish = []
            for index in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(index, 0).findChild(type(QCheckBox())).isChecked():
                    active.append(True)
                else:
                    active.append(False)

                if self.tableWidget.cellWidget(index, 2).findChild(type(QCheckBox())).isChecked():
                    Vegetarian.append(True)
                else:
                    Vegetarian.append(False)

                Dish.append(self.tableWidget.item(index, 1).text())

            df = pd.DataFrame()
            df["active"] = active
            df["Dish"] = Dish
            df["Vegetarian"] = Vegetarian
            df.to_csv("meals.csv", index=True)

            save_text.setHidden(False)
            QTimer.singleShot(2000, hide_again)

        def hide_again():
            save_text.setHidden(True)



        miniwindow = QWidget()
        meal_btn = QPushButton("Add Meal")
        save_btn = QPushButton("Save Changes")
        layout = QHBoxLayout()
        layout.addWidget(meal_btn)
        layout.addWidget(save_btn)
        miniwindow.setLayout(layout)

        save_text = QLabel("All changes saved.")
        save_text.setAlignment(Qt.AlignHCenter)
        save_text.setAlignment(Qt.AlignRight)
        save_text.setMargin(3)
        save_text.setFixedHeight(22)
        save_text.setStyleSheet("QLabel {background-color : rgb(0,77,255); color : white}")
        save_text.setHidden(True)

        ### Button Functions ###
        meal_btn.clicked.connect(add_meal)
        save_btn.clicked.connect(save_table)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(save_text)
        self.layout.addWidget(miniwindow)

        # self.layout.addWidget(self)
        self.setLayout(self.layout)
        self.centro()

        # Show widget
        self.show()

    def createTable(self):
        df = pd.read_csv("meals.csv")
        df.sort_values(by=["active"], ascending=[False], inplace=True)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1] - 1)
        header = self.tableWidget.horizontalHeader()
        self.tableWidget.setHorizontalHeaderLabels(["Active", "Dish", "Vegetarian"])
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)


        for rows in range(0, df.shape[0]):
            qwidget = QWidget()
            checkbox = QCheckBox()
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.setAlignment(Qt.AlignCenter)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setContentsMargins(0, 0, 0, 0)
            if df.iloc[rows, 1]:
                checkbox.setChecked(True)
                self.tableWidget.setCellWidget(rows, 0, qwidget)
            else:
                checkbox.setChecked(False)
                self.tableWidget.setCellWidget(rows, 0, qwidget)

        for rows in range(0, df.shape[0]):
            self.tableWidget.setItem(rows, 1, QTableWidgetItem((df.iloc[rows, 2])))

        for rows in range(0, df.shape[0]):
            qwidget = QWidget()
            checkbox = QCheckBox()
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.setAlignment(Qt.AlignCenter)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setContentsMargins(0, 0, 0, 0)
            if df.iloc[rows, 3]:
                checkbox.setChecked(True)
                self.tableWidget.setCellWidget(rows, 2, qwidget)
            else:
                checkbox.setChecked(False)
                self.tableWidget.setCellWidget(rows, 2, qwidget)

        # self.tableWidget.move(0, 0)



    def centro(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
