import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget,
                             QSlider, QLabel, QDateTimeEdit)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        btn = QPushButton('Button', self)
        btn.setToolTip("Select a date range for suggestions")
        btn.resize(btn.sizeHint())
        btn.move(10, 10)

        sld = QSlider(Qt.Horizontal, self)
        sld.setToolTip("The ratio of vegetarian dishes in the next list of suggestions")
        sld.setMinimum(0)
        sld.setMaximum(100)
        sld.setValue(70)
        sld.move(120, 15)

        ql = QLabel("Veg Dishes " + str(sld.value()) + "%", self)
        ql.move(118, 30)

        def onChanged():
            text = "Veg Dishes " + str(sld.value()) + "%"
            ql.setText(text)
            ql.adjustSize()

        sld.valueChanged.connect(onChanged)

        ds = QDateTimeEdit(self)
        ds.setCalendarPopup(True)
        ds.setMinimumDate(QDate.currentDate())
        ds.setDisplayFormat("ddd dd.MM")
        ds.setToolTip("Select a starting date")
        ds.move(10, 70)
        ds.resize(90, 25)
        ds_lab = QLabel("Start:", self)
        ds_lab.move(10, 55)

        de = QDateTimeEdit(self)
        de.setCalendarPopup(True)
        de.setDate(QDate.currentDate().addDays(5))
        de.setMinimumDate(QDate.currentDate().addDays(0))
        de.setDisplayFormat("ddd dd.MM")
        de.setToolTip("Select an end date")
        de.move(120, 70)
        de.resize(90, 25)

        de_lab = QLabel("End:", self)
        de_lab.move(120, 55)

        def startrange():
            if de.date() < ds.date():
                ds.setDate(de.date())

        de.dateChanged.connect(startrange)

        self.resize(300, 150)
        self.center()
        self.setWindowTitle('Meal Suggestions')
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


# app = QApplication(sys.argv)
#
# window = QWidget()
# window.setWindowTitle("Test123")
#
#
#
# window.show()
# sys.exit(app.exec_())

