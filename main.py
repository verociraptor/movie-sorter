# This Python file uses the following encoding: utf-8
import sys
import os

from MovieServer import movie_sorter as ms
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

#static data to test list view functionality
#TODO: connect to database
list = [["Kiki", "2018"], ["Mononoke", "2019"],
        ["M", "2017"], ["K", "2019"],
        ["Mark", "2016"], ["Mocie2", "2011"],
        ["Tiff", "2015"], ["Moke", "2012"],
        ["Balogna", "2014"], ["Movie3", "2010"],
        ["Hanna", "2013"], ["Movie4", "2009"],
        ["Movie", "2012"], ["Movie5", "2008"]]

class MovieItem(QWidget):
    """
    Custom widget to create the list view of movies in
    the search page
    TODO: attach all other info of movie and maybe make it prettier
    """
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

#No longer really needed bc figured out how to list movies using the listwidget
#containing custom widgets
#class ItemsList(QWidget):
#    def __init__(self, items):
#        super(ItemsList, self).__init__()
#        self.init_widget(items)

#    def init_widget(self, items):
#        #creates box to list all items
#        listBox = QVBoxLayout(self)
#        self.setLayout(listBox)

#        #makes the list box scrollable and resizeable to fit space
#        scroll = QScrollArea(self)
#        listBox.addWidget(scroll)
#        scroll.setWidgetResizable(True)

#        scrollContent = QWidget(scroll)

#        scrollLayout = QVBoxLayout(scrollContent)
#        scrollContent.setLayout(scrolLLayout)
#        for item in items:
#            scrollLayout.addWidget(item)
#        scroll.setWidget(scrollContent)


class MovieApp(QWidget):
    """
    App widget to start the whole app.
    Sets the buttons and movie views, and
    gets the default ui made.
    """
    def __init__(self):
        super(MovieApp, self).__init__()
        self.ui = self.load_ui()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.toSearchPage.clicked.connect(lambda:  self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.mainMenuButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.init_movies_view()


    def init_movies_view(self):
        for i in list:
            movie = MovieItem(i[0], i[1])
            myQListItem = QListWidgetItem(self.ui.listWidget)
            myQListItem.setSizeHint(movie.sizeHint())
            self.ui.listWidget.addItem(myQListItem)
            self.ui.listWidget.setItemWidget(myQListItem, movie)

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
