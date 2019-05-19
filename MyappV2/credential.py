# user enter credential
# check credential
# if true open mainwindow and store pc id
# close license

import sys
import webbrowser

from PyQt5.QtCore import QSharedMemory
from PyQt5 import QtCore, QtGui, QtWidgets, uic


# UI.py 1) import ui
# from ui import


# UI   FORMAT
class License_class(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("ui/License.ui", self)

# UI.py FORMAT 2) inherit ui class at first paramiter
# class Software_class(UI_software.Ui_Dialog,QtWidgets.QDialog):
#     def __init__(self):
#         #UI.py 3) make a super
#         super(UI_software.Ui_Dialog,self).__init__()
#         self.setupUi(self)
#         QtCore.QCoreApplication.processEvents()

        self.pb_apply.clicked.connect(self.check_credential)

    def check_credential(self):
        email = str(self.le_username.text()).strip()
        password = str(self.le_password.text()).strip()

        # if email and password == true: todo
        #     open mainwindow
        # else:
        #     reply = QtWidgets.QMessageBox.information(self, 'Dear User', "You are not register,\n"
        #                                                                     "would you like to register",
        #                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        #                                               QtWidgets.QMessageBox.Yes)
        #     if reply == QtWidgets.QMessageBox.Yes:
        #         # IF "YES" DOWNLOAD AND EXECUTE FILE WITH PROGRESSBAR/ IMPORT PROGRESS.PY
        #         webbrowser.open('https://vetogram.com/register', new=2)
        #     else:
        #         # IF "NO" CLOSE MESSAGEBOX
        #         pass

        print("email:", email, "password:", password)


    def message(self):
        QtWidgets.QMessageBox.information(self, "info", "Vetogram application are currently running")

class MemoryCondition:
    def __init__(self, key='memory_condition_key'):
        self._shm = QSharedMemory(key)
        if not self._shm.attach():
            if not self._shm.create(1):
                raise RuntimeError('error creating shared memory: %s' %
                                   self._shm.errorString())
        self.condition = False

    def __enter__(self):
        self._shm.lock()
        if self._shm.data()[0] == b'\x00':
            self.condition = True
            self._shm.data()[0] = b'\x01'
        self._shm.unlock()
        return self.condition

    def __exit__(self, exc_type, exc_value, traceback):
        if self.condition:
            self._shm.lock()
            self._shm.data()[0] = b'\x00'
            self._shm.unlock()


if __name__ == "__main__":

    with MemoryCondition() as condition:
        app = QtWidgets.QApplication(sys.argv)
        License = License_class()

        if condition:
            License.show()
            sys.exit(app.exec())
        else:
            License.message()
