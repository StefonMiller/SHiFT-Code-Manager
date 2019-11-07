from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt5.uic.properties import QtWidgets, QtCore
import gspread
from PyQt5.QtCore import pyqtSlot, QSize, QRect
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


# Popup window for alerts
class PopUp(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.label = QLabel("")
        self.button = QPushButton("Ok")
        self.button.clicked.connect(self.closed)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.setWindowTitle("Error")

    def closed(self):
        self.close()


# Main window of the GUI
# This UI consists of a main stackedWidget that switches to widgets depending on user actions
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Load ui from ui file
        super(Ui, self).__init__()
        uic.loadUi('shiftdb.ui', self)
        # Addbutton - button that takes us to the UI to add a code.  Connected to addCode
        self.addButton = self.findChild(QtWidgets.QPushButton, 'addButton')
        self.addButton.clicked.connect(self.addCode)
        # Viewbutton - button that takes us to the UI to view all codes.  Connected to viewCodes
        self.viewButton = self.findChild(QtWidgets.QPushButton, 'viewButton')
        self.viewButton.clicked.connect(self.viewCodes)
        # stack - stackedWidget containing all Widgets representing screens
        self.stack = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        # addReturn - button to return to the main menu from adding a code. Connected to menuReturn
        self.addReturn = self.findChild(QtWidgets.QPushButton, 'Return')
        self.addReturn.clicked.connect(self.menuReturn)
        # viewReturn - button to return to the main menu from viewing codes.  Connected to menuReturn
        self.viewReturn = self.findChild(QtWidgets.QPushButton, 'viewReturn')
        self.viewReturn.clicked.connect(self.menuReturn)
        # viewText - QLabel storing all codes in our database
        self.viewText = self.findChild(QtWidgets.QLabel, 'label_2')
        # submit - button user presses when they want to submit a code.  Connected to testVals
        self.submit = self.findChild(QtWidgets.QPushButton, 'Submit')
        self.submit.clicked.connect(self.testVals)
        # date - QDateEdit for user to enter the date
        self.date = self.findChild(QtWidgets.QDateEdit, 'date')
        # code 1-5 - QLineEdits for user to enter the code in 5 pieces
        self.code1 = self.findChild(QtWidgets.QLineEdit, 'code1')
        self.code2 = self.findChild(QtWidgets.QLineEdit, 'code2')
        self.code3 = self.findChild(QtWidgets.QLineEdit, 'code3')
        self.code4 = self.findChild(QtWidgets.QLineEdit, 'code4')
        self.code5 = self.findChild(QtWidgets.QLineEdit, 'code5')
        # codes, exps, ids, dates, rewards - fields to display database items
        self.codes = self.findChild(QtWidgets.QLabel, 'codes')
        self.dates = self.findChild(QtWidgets.QLabel, 'dates')
        self.exps = self.findChild(QtWidgets.QLabel, 'exps')
        self.ids = self.findChild(QtWidgets.QLabel, 'ids')
        self.rewards = self.findChild(QtWidgets.QLabel, 'rewards')
        # expired - QLineEdit for user to tell us whether the code is expired or not
        self.expired = self.findChild(QtWidgets.QComboBox, 'expired')
        # reward - QLineEdit for user to enter the reward
        self.reward = self.findChild(QtWidgets.QLineEdit, 'reward')
        # popup - variable for future popups
        self.popup = None
        # index - number of rows in our spreadsheet
        self.index = len(sheet.col_values(1)) + 1
        self.show()

    # Takes us to the addCode widget in our stackedwidget
    def addCode(self):
        self.stack.setCurrentIndex(2)

    # Takes us to the viewCodes widget in our stackedwidget
    def viewCodes(self):
        # get data from the sheet and fill the qLabels
        self.stack.setCurrentIndex(1)
        codes = sheet.col_values(2)
        dates = sheet.col_values(3)
        expired = sheet.col_values(5)
        ID = sheet.col_values(1)
        rewards = sheet.col_values(4)
        for x in range(len(codes)):
            temp = self.ids.text()
            temp += (str(ID[x]) + "\n")
            self.ids.setText(temp)
            temp = self.codes.text()
            temp += (str(codes[x]) + "\n")
            self.codes.setText(temp)
            temp = self.dates.text()
            temp += (str(dates[x]) + "\n")
            self.dates.setText(temp)
            temp = self.rewards.text()
            temp += (str(rewards[x]) + "\n")
            self.rewards.setText(temp)
            temp = self.exps.text()
            temp += (str(expired[x]) + "\n")
            self.exps.setText(temp)

    # Return to the main menu of our stackedwidget
    def menuReturn(self):
        self.stack.setCurrentIndex(0)

    # Test values in the Line/Date edits for validity and if valid, append a new code entry
    def testVals(self):
        # Fill an array with all fields the user entereed
        tempEntry = []
        tempEntry.append(self.index)
        tempCodes = [self.code1.text(), self.code2.text(), self.code3.text(), self.code4.text(), self.code5.text()]
        # Make sure all code parts are not blank, contain only numbers and characters, and are appropriate length
        for x in tempCodes:
            if x == '' or (not x.isalnum()) or (not len(x) == 5):
                self.correctAns("One or more of the code fields is either blank, too short, or not valid.  Try again")
                return
        tempStr = self.code1.text() + "-" + self.code2.text() + "-" + self.code3.text() + "-" + self.code4.text() + "-" + self.code5.text()
        tempEntry.append(tempStr)
        tempEntry.append(self.date.text())
        tempEntry.append(self.reward.text())
        tempEntry.append(self.expired.currentText())
        # If any index is blank, the entry is not valid
        for x in tempEntry:
            if x == '':
                self.correctAns("One or more of the fields is blank, try again")
                return

        # If we do not return, append a new code and clear the entry fields
        sheet.insert_row(tempEntry, self.index)
        self.index += 1
        self.code1.clear()
        self.code2.clear()
        self.code3.clear()
        self.code4.clear()
        self.code5.clear()
        self.reward.clear()
        # Let user know code entry was successful
        self.popup = PopUp()
        self.popup.setGeometry(QRect(960, 540, 100, 100))
        self.setWindowTitle("Success!")
        self.popup.label.setText("Code added successfully!")
        self.popup.show()

    # Prints a unique error message
    def correctAns(self, err):
        print("called")
        self.popup = PopUp()
        self.popup.setGeometry(QRect(960, 540, 100, 100))
        self.popup.label.setText(str(err))
        self.popup.show()


# Authenticate google profile to allow reading and editing spreadsheet
sheet = authenticate()
# Create GUI
app = QtWidgets.QApplication(sys.argv)
win = Ui()
sys.exit(app.exec_())
