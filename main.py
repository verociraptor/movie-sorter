# This Python file uses the following encoding: utf-8
import sys
import os

from MovieServer import movie_sorter as ms
from MovieServer import movie_sorter_server as server
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class test627(QWidget):


    def __init__(self):
        super(test627, self).__init__()
        self.ui = self.load_ui()
        self.clickedConnect = False   # has user clicked connect ?
        self.ui.dirPath.setReadOnly(True)
        self.ui.status.setReadOnly(True)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.toSearchPage.clicked.connect(lambda:  self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.mainMenuButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.connectCache.clicked.connect(self.connect_to_local_cache)
        self.ui.createCache.clicked.connect(self.create_local_cache)
        self.ui.browseDirectories.clicked.connect(self.browse_directories)
        self.ui.exportMovies.clicked.connect(self.export_movies)

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def create_local_cache(self):
        try:
            server.Create_Local_Cache()
            self.ui.status.setText("Sucessfully created local cache")
        except:
            self.ui.status.setText("Error: cache already exists!")


    def connect_to_local_cache(self):
        try:
            server.Connect_to_Local_Cache()
            self.ui.status.setText("Successfully connected to local cache")
            self.clickedConnect = True
        except:
            self.ui.status.setText("Create a cache first!")

    def browse_directories(self):
        dirName = QFileDialog.getExistingDirectory()
        self.ui.dirPath.setText(dirName)

    def export_movies(self, clickedConnect):
        dirName = self.ui.dirPath.text()
        if self.clickedConnect is False :
            self.ui.status.setText("Connect to your local cache first!")
        elif len(dirName) == 0:
            self.ui.status.setText("No directory selected!")
        else :
            server.export_to_SQLMoviesTable(dirName)
            self.ui.status.setText("Movies successfully exported")


if __name__ == "__main__":
    app = QApplication([])
    widget = test627()
    widget.show()
    sys.exit(app.exec_())
