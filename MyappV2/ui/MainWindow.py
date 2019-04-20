# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(970, 591)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_run = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_run.setGeometry(QtCore.QRect(470, 10, 93, 28))
        self.pushButton_run.setObjectName("pushButton_run")
        self.groupBox_follow_from_hashtag = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_follow_from_hashtag.setGeometry(QtCore.QRect(30, 120, 891, 91))
        self.groupBox_follow_from_hashtag.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.groupBox_follow_from_hashtag.setStyleSheet("#groupBox:checked{\n"
"background-color: rgb(9, 177, 243);\n"
"}\n"
"#groupBox:unchecked{\n"
"background-color: rgb(204, 204, 204);\n"
"}")
        self.groupBox_follow_from_hashtag.setFlat(False)
        self.groupBox_follow_from_hashtag.setCheckable(True)
        self.groupBox_follow_from_hashtag.setChecked(True)
        self.groupBox_follow_from_hashtag.setObjectName("groupBox_follow_from_hashtag")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_follow_from_hashtag)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_10 = QtWidgets.QLabel(self.groupBox_follow_from_hashtag)
        self.label_10.setStyleSheet("background-color:transparent;")
        self.label_10.setTextFormat(QtCore.Qt.AutoText)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.lineEdit_follow_from_hashtag = QtWidgets.QLineEdit(self.groupBox_follow_from_hashtag)
        self.lineEdit_follow_from_hashtag.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_follow_from_hashtag.setText("")
        self.lineEdit_follow_from_hashtag.setObjectName("lineEdit_follow_from_hashtag")
        self.horizontalLayout_5.addWidget(self.lineEdit_follow_from_hashtag)
        self.label_11 = QtWidgets.QLabel(self.groupBox_follow_from_hashtag)
        self.label_11.setAutoFillBackground(False)
        self.label_11.setStyleSheet("background-color:transparent;")
        self.label_11.setWordWrap(False)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.spinBox__follow_from_hashtag = QtWidgets.QSpinBox(self.groupBox_follow_from_hashtag)
        self.spinBox__follow_from_hashtag.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spinBox__follow_from_hashtag.setMaximum(100000)
        self.spinBox__follow_from_hashtag.setObjectName("spinBox__follow_from_hashtag")
        self.horizontalLayout_5.addWidget(self.spinBox__follow_from_hashtag)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_5)
        self.lineEdit_username = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_username.setGeometry(QtCore.QRect(120, 10, 136, 22))
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(12, 12, 91, 31))
        self.label.setStyleSheet("font: 12pt \"Times New Roman\";")
        self.label.setObjectName("label")
        self.lineEdit_password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_password.setGeometry(QtCore.QRect(290, 10, 137, 22))
        self.lineEdit_password.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 70, 264, 28))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(350, 70, 164, 28))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.spinBox_2 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_2.addWidget(self.spinBox_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 970, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label_2.setBuddy(self.spinBox)
        self.label_3.setBuddy(self.spinBox_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_run.setText(_translate("MainWindow", "Run"))
        self.groupBox_follow_from_hashtag.setTitle(_translate("MainWindow", "Follow From Hashtag"))
        self.label_10.setText(_translate("MainWindow", "#"))
        self.lineEdit_follow_from_hashtag.setPlaceholderText(_translate("MainWindow", "tag1,tag2,tag3"))
        self.label_11.setText(_translate("MainWindow", "Amount"))
        self.lineEdit_username.setPlaceholderText(_translate("MainWindow", "username"))
        self.label.setText(_translate("MainWindow", "Vetogram"))
        self.lineEdit_password.setPlaceholderText(_translate("MainWindow", "password"))
        self.label_2.setText(_translate("MainWindow", "Maximum Follow Per Day"))
        self.label_3.setText(_translate("MainWindow", "Follow Delay"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

