import PyQt5
from PyQt5.uic.properties import QtWidgets, QtCore

import gspread
from PyQt5.QtCore import pyqtSlot, QSize
from oauth2client.service_account import ServiceAccountCredentials
from PyQt5 import QtWidgets, uic
import sys


def authenticate():
    # Create a client to interact with googleAPI using the credentials in our credentials.json file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the worksheet containing our shift codes
    return client.open("SHiFT Codes").sheet1

class Ui(QtWidgets.QMainWindow):
        def __init__(self):
            super(Ui, self).__init__()
            uic.loadUi('shiftdb.ui', self)
            self.addButton = self.findChild(QtWidgets.QPushButton, 'addButton')
            self.addButton.clicked.connect(self.addCode)
            self.viewButton = self.findChild(QtWidgets.QPushButton, 'viewButton')
            self.viewButton.clicked.connect(self.viewCodes)
            self.stack = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
            self.addReturn = self.findChild(QtWidgets.QPushButton, 'Return')
            self.addReturn.clicked.connect(self.menuReturn)
            self.viewReturn = self.findChild(QtWidgets.QPushButton, 'Return_2')
            self.viewReturn.clicked.connect(self.menuReturn)
            self.viewText = self.findChild(QtWidgets.QLabel, 'label_2')
            self.submit = self.findChild(QtWidgets.QPushButton, 'Submit')
            self.submit.clicked.connect(self.testVals)
            self.date = self.findChild(QtWidgets.QDateEdit, 'dateEdit')
            self.code = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
            self.expired = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
            self.reward = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
            self.show()
        def addCode(self):
            self.stack.setCurrentIndex(2)

        def viewCodes(self):
            self.stack.setCurrentIndex(1)
            codes = sheet.col_values(2)
            dates = sheet.col_values(3)
            expired = sheet.col_values(5)
            ID = sheet.col_values(1)
            rewards = sheet.col_values(4)
            index = len(codes)
            tempstr = "ID\tCode\t\tDate\t\tReward\tExpired"
            for x in range(len(codes)):
                tempstr += ("\n" + ID[x] + "\t" + codes[x] + "\t" + dates[x] + "\t" + rewards[x] + "\t" + expired[x])
            self.viewText.setText(tempstr)
        def menuReturn(self):
            self.stack.setCurrentIndex(0)
        def testVals(self):
            tempEntry = []
            temp = self.expired.text()
            temp = temp.lower()
            if(temp != 'yes' || temp != 'no' || temp != 'y' || temp != 'no'):
                self.correctAns()
            else:
                tempEntry.append(temp)
            temp = self.code.text()
            if():
                pass
            temp = self.reward.text()
            if():
                pass

            sheet.insert_row(tempEntry, (sheet.row_count + 1))
        def correctAns(self):
            pass
sheet = authenticate()
app = QtWidgets.QApplication(sys.argv)
win = Ui()
sys.exit(app.exec_())
