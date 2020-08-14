# This Python file uses the following encoding: utf-8
import sys
import os

from MovieServer import movie_sorter as ms
from MovieServer import movie_sorter_server as server
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class test627(QWidget):
    def __init__(self):
        super(test627, self).__init__()
        self.ui = self.load_ui()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.toSearchPage.clicked.connect(lambda:  self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.mainMenuButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.connectCache.clicked.connect(lambda: server.Connect_to_Local_Cache())
        self.ui.createCache.clicked.connect(lambda: server.Create_Local_Cache())

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

if __name__ == "__main__":
    app = QApplication([])
    widget = test627()
    widget.show()
    sys.exit(app.exec_())
