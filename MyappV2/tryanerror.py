import sys

from PyQt5.QtCore import QFileInfo, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QFormLayout, QLineEdit, QTabWidget, QWidget, QAction


def restore(settings):
    finfo = QFileInfo(settings.fileName())

    if finfo.exists() and finfo.isFile():
        for w in qApp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    val = settings.value("{}/{}".format(w.objectName(), name), w.property(name))
                    w.setProperty(name, val)


def save(settings):
    for w in qApp.allWidgets():
        mo = w.metaObject()
        if w.objectName() != "":
            for i in range(mo.propertyCount()):
                name = mo.property(i).name()
                settings.setValue("{}/{}".format(w.objectName(), name), w.property(name))


class mainwindow(QMainWindow):
    settings = QSettings("gui.ini", QSettings.IniFormat)

    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.initUI()

        restore(self.settings)

    def initUI(self):
        exitAction = QAction(QIcon('icon\\exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setMovable(False)
        self.toolbar.addAction(exitAction)

        self.tab_widget = QTabWidget(self)  # add tab
        self.tab_widget.setObjectName("tabWidget")

        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")
        self.tab_widget.addTab(self.tab2, "Tab_2")
        self.tab2UI()

        self.setCentralWidget(self.tab_widget)

    def tab2UI(self):
        self.layout = QFormLayout()
        nameLe = QLineEdit(self)
        nameLe.setObjectName("nameLe")
        self.layout.addRow("Name", nameLe)

        addressLe = QLineEdit()
        addressLe.setObjectName("addressLe")
        self.layout.addRow("Address", addressLe)

        self.tab2.setLayout(self.layout)

    def closeEvent(self, event):
        save(self.settings)
        QMainWindow.closeEvent(self, event)


def main():
    app = QApplication(sys.argv)
    ex = mainwindow()
    ex.setGeometry(100, 100, 1000, 600)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()