
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5.uic.properties import QtWidgets, QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


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
import csv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import QSettings, QFileInfo
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QFormLayout, QLineEdit, QTabWidget, QWidget, QAction

from ui import MainWindow

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

path = os.path.expanduser("~\Testing\\")
package = 0 #0=free 1=purchased


# SAVE AND RESTORE LAST USER INPUT
# FUNC ( restore, save, Mainwindow_class.setting, closeEvent)
def restore(settings):
    finfo = QtCore.QFileInfo(settings.fileName())
    if finfo.exists() and finfo.isFile():
        for w in QtWidgets.qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() and not w.objectName().startswith("qt_"):
                settings.beginGroup(w.objectName())
                for i in range( mo.propertyCount(), mo.propertyOffset()-1, -1):
                    prop = mo.property(i)
                    if prop.isWritable():
                        name = prop.name()
                        val = settings.value(name, w.property(name))
                        if str(val).isdigit():
                            val = int(val)
                        w.setProperty(name, val)
                settings.endGroup()

def save(settings):
    for w in QtWidgets.qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() and not w.objectName().startswith("qt_"):
            settings.beginGroup(w.objectName())
            for i in range(mo.propertyCount()):
                prop = mo.property(i)
                name = prop.name()
                if prop.isWritable():
                    settings.setValue(name, w.property(name))
            settings.endGroup()


# UI FORMAT
class MainWindow_class(QtWidgets.QMainWindow):
    #RESTORE FILE LOCATION NAME

    def __init__(self):
        QtCore.QCoreApplication.processEvents()
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("ui/MainWindow.ui", self)

# PY FORMAT
# class MainWindow_class(MainWindow.Ui_MainWindow,QtWidgets.QMainWindow):
#     def __init__(self):
#         super(MainWindow.Ui_MainWindow, self).__init__()
#         self.setupUi(self)

        self.settings = QSettings(path + "gui.ini", QSettings.IniFormat)


        restore(self.settings)

        # OFFICIAL
        self.pushButton_run.clicked.connect(self.login_instagram)
        self.pushButton_update_status.connect(self.update_account_status)

        self.comboBox_follow.currentIndexChanged.connect(self.update_label_follow)

        self.radioButton_slow.clicked.connect(self.rButton_slow)
        self.radioButton_standard.clicked.connect(self.rButton_standard)
        self.radioButton_fast.clicked.connect(self.rButton_fast)

        self.checkBox_private.clicked.connect(self.coming_soon)
        self.checkBox_no_profilePic.clicked.connect(self.coming_soon)
        self.checkBox_business.clicked.connect(self.coming_soon)
        self.checkBox_verified.clicked.connect(self.coming_soon)

        #   TESTING
        # self.pushButton_run.clicked.connect(self.append_csv)
        # self.pushButton.clicked.connect(self.enable_tab)
        # self.pushButton_stop.clicked.connect(self.plot_graph)

        #  SHOW OUTPUT IN QTextEdit
        stdout = OutputWrapper(self, True)
        stdout.outputWritten.connect(self.handleOutput)
        stderr = OutputWrapper(self, False)
        stderr.outputWritten.connect(self.handleOutput)

        # PASS UI OBJECT NAME TO WORKTHREAD CLASS
        self.workThread = workThread(groupBox_follow=self.groupBox_follow,
                                     comboBox_follow=self.comboBox_follow,
                                     lineEdit_follow=self.lineEdit_follow,
                                     spinBox_getfollowers=self.spinBox_getfollowers,
                                     spinBox_getfollowing=self.spinBox_getfollowing,
                                     )

        self.Canvas = Canvas(groupBox_2=self.groupBox_2,)

    def closeEvent(self, event):
        save(self.settings)
        QtWidgets.QMainWindow.closeEvent(self, event)

    def create_path(self):
        base_path = self.return_base_path()
        if not os.path.exists(base_path):
            if not os.path.exists(path):
                os.mkdir(path)
                os.mkdir(base_path)
            else:
                os.mkdir(base_path)
        else:
            pass

    def return_base_path(self):
        base_path = path + self.username() + "\\"
        return base_path

    def username(self):
        username = str(self.lineEdit_username.text()).lower().strip()
        return username

    def csv_file_path(self):
        csv_file = str(self.return_base_path() + "{}.csv".format(self.username()))
        return csv_file

    def setting(self):
        global bot
        bot = Bot(
                 base_path=self.return_base_path(),
                 # proxy=None,
                 max_likes_per_day=self.spinBox_like.value(),
                 # max_unlikes_per_day=1000,
                 max_follows_per_day=self.spinBox_follow.value(),
                 max_unfollows_per_day=self.spinBox_unfollow.value(),
                 max_comments_per_day=self.spinBox_comment.value(),
                 # max_blocks_per_day=100,
                 # max_unblocks_per_day=100,
                 # max_likes_to_like=10000,
                 # min_likes_to_like=2,
                 # max_messages_per_day=300,
                 filter_users=False,
                 filter_private_users=False,
                 filter_users_without_profile_photo=False,
                 filter_previously_followed=False,
                 filter_business_accounts=False,
                 filter_verified_accounts=False,
                 # max_followers_to_follow=2000,
                 # min_followers_to_follow=10,
                 # max_following_to_follow=2000,
                 # min_following_to_follow=10,
                 # max_followers_to_following_ratio=10,
                 # max_following_to_followers_ratio=2,
                 # min_media_count_to_follow=3,
                 # max_following_to_block=2000,
                 like_delay=40,
                 # unlike_delay=10,
                 follow_delay=60,
                 unfollow_delay=60,
                 comment_delay=120,
                 # block_delay=30,
                 # unblock_delay=30,
                 message_delay=90,
                 # stop_words=('shop', 'store', 'free'),
                 # blacklist_hashtags=['#shop', '#store', '#free'],
                 # blocked_actions_protection=True,
                 # verbosity=True,
                 # device=None)
                )

    def login_instagram(self):
        QtCore.QCoreApplication.processEvents()
        self.create_path()
        self.setting()

        password = str(self.lineEdit_password.text()).strip()

        if bot.login(username=self.username(), password=password) == 1:
            # ALL TASK START HERE AFTER LOGIN
            self.csv_check()
            self.update_account_status()
            self.workThread.start()

        else:
            QtWidgets.QMessageBox.warning(self, "Ooopps", "wrong username or password")

    # TESTING
    def click_start(self):
        # # self.workThread.start()
        # QtCore.QCoreApplication.processEvents()
        # try:
        #     self.tabWidget.setTabEnabled(1,False)
        # except:
        #     pass
        # # time.sleep(2)
        # print(self.lineEdit.text())
        print(self.csv_file_path())
    def enable_tab(self):
        self.tabWidget.setTabEnabled(1, True)


    def csv_check(self): #success create csv file
        if not os.path.exists(self.csv_file_path()):
            with open(self.csv_file_path(), "w") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(['dateTime', 'followers'])
        else:
            self.csv_append()

    def csv_append(self):
        with open(self.csv_file_path(), "a") as csvFile:
            writer = csv.writer(csvFile)
            data = bot.save_user_stats(self.username())
            user_followers = str(data['followers'])
            user_dateTime = str(data['date'])
            writer.writerow([user_dateTime, user_followers])



    def coming_soon(self):
        QtWidgets.QMessageBox.information(self, "info", "Coming Soon don't forget to purchase full package")

    def update_label_follow(self):
        combobox = self.comboBox_follow.currentText()
        if combobox == "hashtags":
            self.label_follow.setText("of hashtag")
            self.lineEdit_follow.setPlaceholderText("tag1,tag2,tag3")

        else:
            self.label_follow.setText("of username")
            self.lineEdit_follow.setPlaceholderText("username1,username2,username3")

    def rButton_slow(self):
        if package == 0:
            QtWidgets.QMessageBox.information(self, "Info", "Grow your instagram fastly just\n"
                                                            "purchase full package to customize your setting")
        else:
            self.spinBox_follow.setValue(50)
            self.spinBox_unfollow.setValue(30)
            self.spinBox_like.setValue(50)
            self.spinBox_comment.setValue(7)
            self.spinBox_getfollowers.setValue(100)
            self.spinBox_getfollowing.setValue(100)

    def rButton_standard(self):
        if package == 0:
            self.radioButton_slow.setChecked(True)
            QtWidgets.QMessageBox.information(self, "Info", "To use this setting you need\n"
                                                              "to purchase full package")

        else:
            self.spinBox_follow.setValue(500)
            self.spinBox_unfollow.setValue(500)
            self.spinBox_like.setValue(750)
            self.spinBox_comment.setValue(50)
            self.spinBox_getfollowers.setValue(1000)
            self.spinBox_getfollowing.setValue(1000)

    def rButton_fast(self):
        if package == 0:
            self.radioButton_slow.setChecked(True)
            QtWidgets.QMessageBox.information(self, "Info", "To use this setting you need\n"
                                                              "to purchase full package")
        else:
            self.spinBox_follow.setValue(1000)
            self.spinBox_unfollow.setValue(1000)
            self.spinBox_like.setValue(1500)
            self.spinBox_comment.setValue(100)
            self.spinBox_getfollowers.setValue(10000)
            self.spinBox_getfollowing.setValue(10000)

            self.spinBox_follow.setReadOnly(False)
            self.spinBox_unfollow.setReadOnly(False)
            self.spinBox_like.setReadOnly(False)
            self.spinBox_comment.setReadOnly(False)
            self.spinBox_getfollowers.setReadOnly(False)
            self.spinBox_getfollowing.setReadOnly(False)

    def handleOutput(self, text, stdout):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertPlainText(text)

    # TAB DASHBOARD
    def update_account_status(self):
        data = bot.save_user_stats(self.username())
        user_following = str(data['following'])
        user_followers = str(data['followers'])

        self.lineEdit_following.setText(user_following)
        self.lineEdit_followers.setText(user_followers)

    #todo
    def update_task_status(self):
        likes = str(bot.total['likes'])
        # follow = str(bot.total['follows'])
        # unfollow = str(bot.total['unfollows'])
        # comment = str(bot.total['comments'])

        # self.lineEdit_total_follow.setText(follow)
        # self.lineEdit_total_unfollow.setText(unfollow)
        # self.lineEdit_total_likes.setText(likes)
        # self.lineEdit_total_comment.setText(comment)

class Canvas(FigureCanvas):
    def __init__(self,groupBox_2, parent=None):
        self.figure = plt.figure()
        FigureCanvas.__init__(self, self.figure)

        self.groupBox_2 = groupBox_2

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.groupBox_2.setLayout(layout) #put the layout in groupbox

    def plot(self):
        import pandas as pd
        MainWindowClass = MainWindow_class()
        path = MainWindowClass.csv_file_path()

        # read data from file
        data = pd.read_csv(path)

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(data.dateTime,data.followers, '*-')
        plt.title("followers over time")
        plt.xlabel("date and time")
        plt.ylabel("followers growth")

        _ = plt.xticks(rotation=45)

        # refresh canvas
        self.canvas.draw()

    #TESTING
    def testing(self):
        MainWindowClass = MainWindow_class()
        print(MainWindowClass.csv_file_path())

# MAKE THREAD SO THAT UI DIDNT FREEZE
class workThread(QtCore.QThread):
    my_signal = QtCore.pyqtSignal()

    def __init__(self,
                 groupBox_follow,
                 comboBox_follow,
                 lineEdit_follow,
                 spinBox_getfollowers,
                 spinBox_getfollowing,
                 parent=None):

        super(workThread, self).__init__(parent)
        # IMPORT UI OBJECT NAME FROM MAINWINDOW CLASS
        self.groupBox_follow = groupBox_follow
        self.comboBox_follow = comboBox_follow
        self.lineEdit_follow = lineEdit_follow
        self.spinBox_getfollowers = spinBox_getfollowers
        self.spinBox_getfollowing = spinBox_getfollowing

    def follow(self):
        # IF THE GROUPBOX IS CHECK, FOLLOW USER WITH THAT #
        if self.groupBox_follow.isChecked() == 1:
            if self.comboBox_follow.currentText() == "hashtags":
                hashtags = str(self.lineEdit_follow.text()).strip().split(",")
                for hashtag in hashtags:
                    # print("Begin hahstag: " + hashtag)
                    users = bot.get_hashtag_users(hashtag)
                    bot.follow_users(users)

            if self.comboBox_follow.currentText() == "followers":
                usernames = str(self.lineEdit_follow.text()).strip().split(",")
                for username in usernames:
                    # print("Begin followers: " + username)
                    bot.follow_followers(username, nfollows=self.spinBox_getfollowers.value())

            if self.comboBox_follow.currentText() == "following":
                usernames = str(self.lineEdit_follow.text()).strip().split(",")
                for username in usernames:
                    # print("Begin following: " + username)
                    bot.follow_following(username,nfollows=self.spinBox_getfollowing.value())
        else:
            print("groupBox_follow_from_hashtag not check")
            pass

    # ALL FUNCTION IN WORKTHREAD START HERE
    def run(self):
        #todo check expired date
        #OFFICIAL
        # self.follow()

        #TESTING
        print("follow task running")


class OutputWrapper(QtCore.QObject):
    """ to show all output in ui text edit"""
    outputWritten = QtCore.pyqtSignal(object, object)

    def __init__(self, parent, stdout=True):
        QtCore.QObject.__init__(self, parent)
        if stdout:
            self._stream = sys.stdout
            sys.stdout = self
        else:
            self._stream = sys.stderr
            sys.stderr = self
        self._stdout = stdout

    def write(self, text):
        self._stream.write(text)
        self.outputWritten.emit(text, self._stdout)

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def __del__(self):
        try:
            if self._stdout:
                sys.stdout = self._stream
            else:
                sys.stderr = self._stream
        except AttributeError:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_class()
    MainWindow.show()
    sys.exit(app.exec_())
