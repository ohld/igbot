# import sys
#
# from PyQt5 import QtWidgets, QtCore
#
# # for PyQt4 change QtWidget to QtGui and PyQt5 to PyQt4
# from PyQt5.QtCore import QSettings
#
#
# def restore(settings):
#     finfo = QtCore.QFileInfo(settings.fileName())
#     if finfo.exists() and finfo.isFile():
#         for w in QtWidgets.qApp.allWidgets():
#             mo = w.metaObject()
#             if w.objectName() and not w.objectName().startswith("qt_"):
#                 settings.beginGroup(w.objectName())
#                 for i in range( mo.propertyCount(), mo.propertyOffset()-1, -1):
#                     prop = mo.property(i)
#                     if prop.isWritable():
#                         name = prop.name()
#                         val = settings.value(name, w.property(name))
#                         if str(val).isdigit():
#                             val = int(val)
#                         w.setProperty(name, val)
#                 settings.endGroup()
#     else:
#         print("nofileinfo")
#
# def save(settings):
#     for w in QtWidgets.qApp.allWidgets():
#         mo = w.metaObject()
#         if w.objectName() and not w.objectName().startswith("qt_"):
#             settings.beginGroup(w.objectName())
#             for i in range(mo.propertyCount()):
#                 prop = mo.property(i)
#                 name = prop.name()
#                 if prop.isWritable():
#                     settings.setValue(name, w.property(name))
#             settings.endGroup()
#
#
# class Widget(QtWidgets.QWidget):
#     # settings = QSettings("gui.ini", QSettings.IniFormat)
#     def __init__(self, parent=None):
#         super(Widget,self).__init__(parent)
#         self.setObjectName("widget")
#         self.init_ui()
#         self.settings = QtCore.QSettings()
#         restore(self.settings)
#
#     def init_ui(self):
#         lay = QtWidgets.QVBoxLayout(self)
#         lineEdit1 = QtWidgets.QLabel("label")
#         lineEdit1.setObjectName("label")
#         lineEdit2 = QtWidgets.QLineEdit()
#         lineEdit2.setObjectName("lineEdit2")
#         combobox = QtWidgets.QComboBox()
#         combobox.addItems(["1", "2", "3"])
#         combobox.setObjectName("combo")
#         lay.addWidget(lineEdit1)
#         lay.addWidget(lineEdit2)
#         lay.addWidget(combobox)
#
#     def closeEvent(self, event):
#         save(self.settings)
#         QtWidgets.QWidget.closeEvent(self, event)
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     QtCore.QCoreApplication.setOrganizationName("Eyllanesc")
#     QtCore.QCoreApplication.setOrganizationDomain("eyllanesc.com")
#     QtCore.QCoreApplication.setApplicationName("MyApp")
#     ex = Widget()
#     ex.show()
#     sys.exit(app.exec_())
import datetime
import os


# followed_file='followed.txt'
# def make_path():
#     os.mkdir(os.path.expanduser("~\Testing\\"))
# def make_file():
#     make_path()
#     base_path = os.path.expanduser("~\Testing\\")
#     with open(os.path.join(base_path, followed_file), "w") as of:
#         of.write("Now the file has more content!")
#
# make_file()


#CREATE PATH
# username = "broamalabro__2.co"
# path = os.path.expanduser("~\Testing\\")
# base_path = os.path.expanduser("~\Testing\\" + username)
# print(path)
# def create_path():
#     if not os.path.exists(base_path):
#         if not os.path.exists(path):
#             os.mkdir(path)
#             os.mkdir(base_path)
#         else:
#             os.mkdir(base_path)
#             print(" base path not exist just created")
#     else:
#         print("dir exist")
#
# create_path()

# #INSERT NEW VALUE
# old_value = 0
# while 1:
#     new_value = int(input("insert new value"))
#     if new_value <= 85:
#
#         total_value = old_value + new_value
#         old_value += new_value
#     else:
#         break
#
#     print(total_value)


# import csv
#
# csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
#
# with open('testing.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(csvData)


# import pandas as pd
# from matplotlib import pyplot as plt
#
# sample_data = pd.read_csv('testing.csv')
# #plot Date Open
# plt.plot(sample_data.Date,sample_data.Open)
# plt.show()


#########################################################################################
# import sys
#
# from PyQt5 import uic
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
# from PyQt5.uic.properties import QtWidgets, QtCore
#
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.pyplot as plt
#
# import random
#
# class Window(QDialog):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#         QDialog.__init__(self)
#         uic.loadUi("ui/Testing.ui", self)
#
#         # a figure instance to plot on
#         self.figure = plt.figure()
#
#         # this is the Canvas Widget that displays the `figure`
#         # it takes the `figure` instance as a parameter to __init__
#         self.canvas = FigureCanvas(self.figure)
#
#         # this is the Navigation widget
#         # it takes the Canvas widget and a parent
#         self.toolbar = NavigationToolbar(self.canvas, self)
#
#         # Just some button connected to `plot` method
#         self.button = QPushButton('Plot')
#         self.button.clicked.connect(self.plot)
#
#         # set the layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.toolbar)
#         layout.addWidget(self.canvas)
#         layout.addWidget(self.button)
#         self.widget.setLayout(layout) #put the layout in groupbox
#
#     def plot(self):
#         ''' plot some random stuff '''
#         # random data
#         data = [random.random() for i in range(1000)]
#
#         # instead of ax.hold(False)
#         self.figure.clear()
#
#         # create an axis
#         ax = self.figure.add_subplot(111)
#
#         # discards the old graph
#         # ax.hold(False) # deprecated, see above
#
#         # plot data
#         ax.plot(data, '*-')
#
#         # refresh canvas
#         self.canvas.draw()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     main = Window()
#     main.show()
#
#     sys.exit(app.exec_())

import sys
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
bot = Bot()
# bot.login(username='vicode.co', password='vicode.co98')
data = bot.save_user_stats("bromalayabro")
user_followers = str(data['followers'])
user_dateTime = str(data['date'])

print(user_followers)
print(user_dateTime)