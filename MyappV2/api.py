import sys

from PyQt5 import QtWidgets

from vetogram import MainWindow_class
from credential import License_class

app = QtWidgets.QApplication(sys.argv)

# todo
def get_package():
    return 1

# todo
def get_expired_at():
    pass

# todo
def check_credential():
    pass

# todo
def logout_app():
    pass

# todo
def check_version_update():
    pass

def open_MainWindow():
    MainWindow = MainWindow_class()
    MainWindow.show()
    sys.exit(app.exec_())

def open_credential():
    License = License_class()
    License.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    pass
