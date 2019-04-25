import sys

from PyQt5 import QtWidgets
from PyQt5 import uic

#IMPORT UI.PY FOLDER



# UI FORMAT
class Dashboard_class(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("ui/Dashboard.ui", self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dashboard = Dashboard_class()  # take from here put (self.) at front
    Dashboard.show()  # import this #class #untill here
    sys.exit(app.exec_())