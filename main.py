# This Python file uses the following encoding: utf-8
import sys
import os

from MovieServer import movie_sorter as ms
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader



class MovieItem(QListWidgetItem):
    def __init__(self, title, year):
        super(MovieItem, self).__init__()
        self.init_widget(title, year)

    def init_widget(self, title, year):
        title = QLabel(title)
        year = QLabel(year)
        movieBox = QHBoxLayout()
        movieBox.addWidget(title)
        movieBox.addWidget(year)
        self.setLayout(movieBox)

class ItemsList(QWidget):
    def __init__(self, items):
        super(ItemsList, self).__init__()
        self.init_widget(items)

    def init_widget(self, items):
        #creates box to list all items
        listBox = QVBoxLayout(self)
        self.setLayout(listBox)

        #makes the list box scrollable and resizeable to fit space
        scroll = QScrollArea(self)
        listBox.addWidget(scroll)
        scroll.setWidgetResizable(True)

        scrollContent = QWidget(scroll)

        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrolLLayout)
        for item in items:
            scrollLayout.addWidget(item)
        scroll.setWidget(scrollContent)


class MovieApp(QWidget):
    def __init__(self):
        super(MovieApp, self).__init__()
        self.ui = self.load_ui()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.toSearchPage.clicked.connect(lambda:  self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.mainMenuButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        for i in range(0, 5):
            self.ui.listWidget.addItem(MovieItem("Jose's Delivery Service", "2018"))


    def init_movies_view(self):
        list = []
        for i in range(0, 5):
            list.append(MovieItem("Jose's Delivery Service", "2018"))
        return ItemsList(list)

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
    widget = MovieApp()
    widget.show()
    sys.exit(app.exec_())
