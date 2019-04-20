import sys

from PyQt5 import QtWidgets, QtCore

# for PyQt4 change QtWidget to QtGui and PyQt5 to PyQt4
from PyQt5.QtCore import QSettings


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
    else:
        print("nofileinfo")

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


class Widget(QtWidgets.QWidget):
    # settings = QSettings("gui.ini", QSettings.IniFormat)
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)
        self.setObjectName("widget")
        self.init_ui()
        self.settings = QtCore.QSettings()
        restore(self.settings)

    def init_ui(self):
        lay = QtWidgets.QVBoxLayout(self)
        lineEdit1 = QtWidgets.QLabel("label")
        lineEdit1.setObjectName("label")
        lineEdit2 = QtWidgets.QLineEdit()
        lineEdit2.setObjectName("lineEdit2")
        combobox = QtWidgets.QComboBox()
        combobox.addItems(["1", "2", "3"])
        combobox.setObjectName("combo")
        lay.addWidget(lineEdit1)
        lay.addWidget(lineEdit2)
        lay.addWidget(combobox)

    def closeEvent(self, event):
        save(self.settings)
        QtWidgets.QWidget.closeEvent(self, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtCore.QCoreApplication.setOrganizationName("Eyllanesc")
    QtCore.QCoreApplication.setOrganizationDomain("eyllanesc.com")
    QtCore.QCoreApplication.setApplicationName("MyApp")
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())