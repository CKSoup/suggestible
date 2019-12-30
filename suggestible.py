import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget,
                             QSlider, QLabel, QDateTimeEdit, QVBoxLayout, QGridLayout)
from PyQt5.QtGui import QIcon
import jinja2
from datetime import timedelta
from dateutil.parser import parse
import webbrowser
from Main import main
import tablegui


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn_gen = QPushButton('Generate', self)
        btn_gen.setToolTip("Generate meal suggestions")
        btn_gen.setStyleSheet('QPushButton {background-color : rgb(255,0,0); color : black}')

        btn_edit = QPushButton('Edit List', self)
        btn_edit.setToolTip("Edit Meals")

        sld = QSlider(Qt.Horizontal, self)
        sld.setToolTip("The ratio of vegetarian dishes in the next list of suggestions")
        sld.setMinimum(0)
        sld.setMaximum(100)
        sld.setValue(70)

        sld_lab = QLabel("Veg Dishes " + str(sld.value()) + "%", self)


        def onChanged():
            text = "Veg Dishes " + str(sld.value()) + "%"
            sld_lab.setText(text)

        sld.valueChanged.connect(onChanged)

        start_cal = QDateTimeEdit(self)
        start_cal.setCalendarPopup(True)
        start_cal.setMinimumDate(QDate.currentDate())
        start_cal.setDisplayFormat("ddd dd.MM")
        start_cal.setToolTip("Select a starting date")
        start_cal_lab = QLabel("Start:", self)

        end_cal = QDateTimeEdit(self)
        end_cal.setCalendarPopup(True)
        end_cal.setDate(QDate.currentDate().addDays(5))
        end_cal.setMinimumDate(QDate.currentDate().addDays(0))
        end_cal.setDisplayFormat("ddd dd.MM")
        end_cal.setToolTip("Select an end date")
        end_cal_lab = QLabel("End:", self)


        def startrange():
            if end_cal.date() < start_cal.date():
                start_cal.setDate(end_cal.date())

        end_cal.dateChanged.connect(startrange)

        self.setFixedSize(300, 150)
        self.center()
        self.setWindowTitle('suggestible')
        self.setWindowIcon(QIcon('icon.png'))

        def createGridLayout(self):
            self.horizontalGroupBox = QWidget()
            layout = QGridLayout()
            layout.setColumnStretch(0, 5)
            layout.setColumnStretch(1, 5)
            layout.setRowStretch(5, 1)
            layout.setVerticalSpacing(8)

            layout.addWidget(start_cal_lab, 0, 0)
            layout.addWidget(end_cal_lab, 0, 1)
            layout.addWidget(start_cal, 1, 0)
            layout.addWidget(end_cal, 1, 1)
            layout.addWidget(btn_edit, 2, 0)
            layout.addWidget(sld, 2, 1)
            layout.addWidget(sld_lab, 2, 1, 3, 1, alignment=Qt.AlignCenter)
            layout.addWidget(btn_gen, 4, 0, 2, 2)
            layout.setRowMinimumHeight(4, 15)
            layout.setRowMinimumHeight(5, 15)

            self.horizontalGroupBox.setLayout(layout)

        createGridLayout(self)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()


        def dates(starting, ending):
            end = ending.date()
            start = starting.date()
            en = end.toString("yyyy-MM-dd")
            en = parse(en)
            st = start.toString("yyyy.MM.dd")
            st = parse(st)

            def daterange(st, en):
                for n in range(int((en - st).days) + 1):
                    yield st + timedelta(n)

            fin_dates = []
            for dt in daterange(st, en):
                fin_dates.append(dt.strftime("%A %d.%m"))

            return fin_dates

        def dates_header(starting, ending):
            end = ending.date()
            start = starting.date()
            en = end.toString("dd.MM")
            st = start.toString("dd.MM")
            return st + "-" + en

        def html_creator(starting, ending, ratio0):
            templateLoader = jinja2.FileSystemLoader(searchpath="")
            templateEnv = jinja2.Environment(loader=templateLoader)
            TEMPLATE_FILE = "template_suggestions.html"
            template = templateEnv.get_template(TEMPLATE_FILE)

            outputText = template.render(range=dates_header(starting, ending), table=main(dates(starting, ending), ratio0))
            html_file = open("suggestions" + '.html', 'w')
            html_file.write(outputText)
            html_file.close()

        def generate():
            html_creator(start_cal, end_cal, sld.value() / 100)
            webbrowser.open("suggestions.html", new=1)

        def popupwindow():
            self.editor = tablegui.App()

        btn_gen.clicked.connect(generate)
        btn_edit.clicked.connect(popupwindow)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())



