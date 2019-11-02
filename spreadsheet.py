import PyQt5
from PyQt5.uic.properties import QtWidgets, QtCore

import gspread
from PyQt5.QtCore import pyqtSlot, QSize
from oauth2client.service_account import ServiceAccountCredentials
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStyleFactory, QHBoxLayout, \
    QLineEdit, QDialog, QVBoxLayout, QSizePolicy, QStyle, QLayout, QStackedWidget
import sys


def authenticate():
    # Create a client to interact with googleAPI using the credentials in our credentials.json file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the worksheet containing our shift codes
    return client.open("SHiFT Codes").sheet1

sheet = authenticate()
codes = sheet.col_values(2)
dates = sheet.col_values(3)
expired = sheet.col_values(5)
ID = sheet.col_values(1)
rewards = sheet.col_values(4)
index = len(codes)
tempstr = "ID\tCode\t\tDate\t\tReward\tExpired"
for x in range(len(codes)):
    tempstr += ("\n" + ID[x] + "\t" + codes[x] + "\t" + dates[x] + "\t" + rewards[x] + "\t" + expired[x])
print(tempstr)
ins = input("Would you like to add a code? Y/N")
while(ins.lower() == "y"):
    temp = []
    temp.append(input("Please enter the code"))
    temp.append(input("Please enter the date"))
    temp.append(input("Please enter the reward"))
    sheet.insert_row(temp, (index + 1))
    ins = input("Would you like to add a code? Y/N")

print("Thank you for using my program")