import os
import random
import shutil
import sys
import time
import threading
import errno
import queue
import requests
import webbrowser
import schedule

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5 import uic

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


# UI FORMAT
class MainWindow_class(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("UI/MainWindow.ui", self)

        # CLICK RUN BUTTON TRIGGER LOGIN FUNCTION
        self.pushButton_run.clicked.connect(self.login_instagram)

        # PASS UI OBJECT NAME TO WORKTHREAD CLASS
        self.workThread = workThread(lineEdit_follow_from_hashtag=self.lineEdit_follow_from_hashtag)

    def login_instagram(self):
        global bot
        bot = Bot()
        username = str(self.lineEdit_username.text()).lower().strip()
        password = str(self.lineEdit_password.text()).strip()
        if bot.login(username=username, password=password) == 1:
            #ALL TASK START HERE AFTER LOGIN
            self.workThread.start()
            #pass
        else:
            QtWidgets.QMessageBox.warning(self, "Ooopps", "wrong username or password")

#MAKE THREAD SO THAT UI DIDNT FREEZE
class workThread(QtCore.QThread):
    my_signal = QtCore.pyqtSignal()
    def __init__(self,lineEdit_follow_from_hashtag,parent=None):
        super(workThread,self).__init__(parent)
        # IMPORT UI OBJECT NAME FROM MAINWINDOW CLASS
        self.lineEdit_follow_from_hashtag = lineEdit_follow_from_hashtag

    def follow_from_hastags(self):
        hashtags = str(self.lineEdit_follow_from_hashtag.text()).strip().split(",")
        for hashtag in hashtags:
            print("Begin following: " + hashtag)
            users = bot.get_hashtag_users(hashtag)
            bot.follow_users(users)

    #ALL FUNCTION IN WORKTHREAD START HERE
    def run(self):
        self.follow_from_hastags()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_class()
    MainWindow.show()
    sys.exit(app.exec_())
