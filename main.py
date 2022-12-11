import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton
import sqlite3


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("project.db")
        self.cur = self.con.cursor()
        self.regionNum = 0
        self.initUI()
        self.region_cb()
        self.cb1.currentTextChanged.connect(self.region_cb)
        self.cb2.currentTextChanged.connect(self.subject_cb)
        self.cb3.currentTextChanged.connect(self.standard_cb)
        self.btn.clicked.connect(self.show_result)

    def initUI(self):
        self.location = QLabel('도시', self)
        self.location.move(50, 30)
        self.subject = QLabel('행정구', self)
        self.subject.move(150, 30)
        self.standard = QLabel('품목', self)
        self.standard.move(300, 30)
        self.standard = QLabel('규격', self)
        self.standard.move(550, 30)

        self.lbl = QLabel(self)
        self.lbl.setFixedWidth(700)
        self.lbl.move(50, 150)

        self.btn = QPushButton('확인', self)
        self.btn.move(800, 250)

        self.cb1 = QComboBox(self)
        self.cb1.move(50, 50)

        self.cb2 = QComboBox(self)
        self.cb2.move(150, 50)

        self.cb3 = QComboBox(self)
        self.cb3.setFixedWidth(200)
        self.cb3.move(300, 50)

        self.cb4 = QComboBox(self)
        self.cb4.setFixedWidth(300)
        self.cb4.move(550, 50)

        self.cur.execute("SELECT DISTINCT city FROM location")
        for row in self.cur.fetchall():
            self.cb1.addItem(row[0])

        self.setWindowTitle('myApp')
        self.setGeometry(50, 50, 1000, 300)
        self.show()

    def region_cb(self):
        self.cb2.blockSignals(True)
        self.cb2.clear()
        self.city = self.cb1.currentText()
        self.cur.execute("SELECT region FROM location WHERE city=?", (self.city,))
        for row in self.cur.fetchall():
            self.cb2.addItem(row[0])
        self.cb2.blockSignals(False)
        self.subject_cb()

    def subject_cb(self):
        self.cb3.clear()
        self.region = self.cb2.currentText()
        self.cur.execute("SELECT regionNum FROM location WHERE city=? AND region=?", (self.city, self.region, ))
        self.regionNum = self.cur.fetchone()[0]
        self.cur.execute("SELECT DISTINCT subject FROM data WHERE regionNum=?", (self.regionNum, ))
        for row in self.cur.fetchall():
            self.cb3.addItem(row[0])
        self.standard_cb()

    def standard_cb(self):
        self.cb4.clear()
        self.subject = self.cb3.currentText()
        self.cur.execute("SELECT standard FROM data WHERE subject=? AND regionNum=?", (self.subject, self.regionNum, ))

        for row in self.cur.fetchall():
            self.cb4.addItem(row[0])

    def show_result(self):
        if self.regionNum:
            self.lbl.clear()
            standard = self.cb4.currentText()
            self.cur.execute("SELECT cost FROM data WHERE subject=? AND standard=? AND regionNum=?", (self.subject, standard, self.regionNum, ))
            text = f"{self.city} {self.region}에서 {self.subject}[{standard}] 처리 수수료는 {self.cur.fetchone()[0]}원이 필요합니다. "
            self.lbl.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyApp()
    app.exec_()
