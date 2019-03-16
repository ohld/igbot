import sys
import os

from PyQt5 import QtWidgets
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

    def login_instagram(self):
        global bot
        bot = Bot()
        username = str(self.lineEdit_username.text()).lower().strip()
        password = str(self.lineEdit_password.text()).strip()
        if bot.login(username=username, password=password) == 1:
            pass
        else:
            QtWidgets.QMessageBox.warning(self, "Ooopps", "wrong username or password")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow_class()
    MainWindow.show()
    sys.exit(app.exec_())
