import sys
import os
from MovieServer import movie_sorter_server as server
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QListWidgetItem
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

moviename = 1


class MovieItem(QWidget):
    """
    Custom widget to create the list view of movies in
    the search page
    TODO: attach all other info of movie and maybe make it prettier
    """
    def __init__(self, title, year, runtime, avgScore):
        super(MovieItem, self).__init__()
        self.init_widget(title, year, runtime, avgScore)

    def init_widget(self, title, year, runtime,avgScore):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.avgScore =avgScore
        movie_title = QLabel(self.title)
        movie_year = QLabel(self.year)
        movie_runtime = QLabel(self.runtime)
        movie_avgScore = QLabel(self.avgScore)
        movieBox = QHBoxLayout()
        movieBox.addWidget(movie_title)
        movieBox.addWidget(movie_year)
        movieBox.addWidget(movie_runtime)
        movieBox.addWidget(movie_avgScore)
        self.setLayout(movieBox)



class MovieApp(QWidget):
    """
    App widget to start the whole app.
    Sets the buttons and movie views, and
    gets the default ui made.
    """
    def __init__(self):
        super(MovieApp, self).__init__()
        self.ui = self.load_ui()
        #self.moviename = 1 # indexing for movies
        self.connect_to_local_cache() # this might be a better way to start the program
        self.clickedConnect = False   # has user clicked connect ?
        self.ui.dirPath.setReadOnly(True)
        self.ui.status.setReadOnly(True)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.connect_buttons()
        self.init_movies_view()

    def connect_buttons(self):
        self.ui.toSearchPage.clicked.connect(lambda:  self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.goBack.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.mainMenuButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.connectCache.clicked.connect(self.connect_to_local_cache)
        self.ui.createCache.clicked.connect(self.create_local_cache)
        self.ui.browseDirectories.clicked.connect(self.browse_directories)
        self.ui.importMovies.clicked.connect(self.import_movies)
        self.ui.search.clicked.connect(self.update_movies_view)


    def init_movies_view(self):
        """
        Sets up default list of movies shown in search page.
        Lists all movies in given local database.
        """
        list = server.get_all_movies(True, False) # default Ascending Alphanumerical order
        #for row in list:
        #        print(row[moviename])
        for col in list:
            movie = MovieItem(col[1], str(col[5]),str(col[9]) + " min", str(col[12]) ) # name and year and runtime
            myQListItem = QListWidgetItem(self.ui.listWidget)
            myQListItem.setSizeHint(movie.sizeHint())
            self.ui.listWidget.addItem(myQListItem)
            self.ui.listWidget.setItemWidget(myQListItem, movie)

        #sets up each movie in search page to be connected to its
        #respective page when clicked on
        self.ui.listWidget.itemClicked.connect(self.movie_clicked)

    def update_movies_view(self):
    #TODO : fix bug where if nothing is selected or if ASC/DESC is only selected - an error is thrown pressing search
        """
        Updates movies in search page with new search queries
        """
        searchtype = None
        if self.ui.avgScore.isChecked() or self.ui.releaseYear.isChecked() or self.ui.runtime.isChecked():
        # for radio buttons, either one or the other will be checked
            searchtype = "filter"
            list = server.apply_filters_ui(self.ui.avgScore.isChecked()
                                            ,self.ui.releaseYear.isChecked()
                                            ,self.ui.runtime.isChecked()
                                            ,self.ui.ASC.isChecked()
                                            ,self.ui.DSC.isChecked())
        if len(self.ui.keyword.text()) != 0: # keyword box has an input
            searchtype = "keyword"
            list = server.keyword_search_ui( self.ui.keyword.text() )

        if searchtype != None:
            self.ui.listWidget.clear() # clears previous items in list

            for col in list:
                movie = MovieItem(col[1], str(col[5]),str(col[9]) + " min",
                                  str(col[12]) )
                                  # name and year and runtime
                myQListItem = QListWidgetItem(self.ui.listWidget)
                myQListItem.setSizeHint(movie.sizeHint())
                self.ui.listWidget.addItem(myQListItem)
                self.ui.listWidget.setItemWidget(myQListItem, movie)

            #sets up each movie in search page to be connected to its
            #respective page when clicked on
            self.ui.listWidget.itemClicked.connect(self.movie_clicked)

        else: # TODO: fix this repetitive code

            list = server.get_all_movies(self.ui.ASC.isChecked()
                                            ,self.ui.DSC.isChecked())
            self.ui.listWidget.clear()
            for col in list:
                movie = MovieItem(col[1], str(col[5]),str(col[9]) + " min",
                                  str(col[12]) )
                                  # name and year and runtime
                myQListItem = QListWidgetItem(self.ui.listWidget)
                myQListItem.setSizeHint(movie.sizeHint())
                self.ui.listWidget.addItem(myQListItem)
                self.ui.listWidget.setItemWidget(myQListItem, movie)

            self.ui.listWidget.itemClicked.connect(self.movie_clicked)

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
            self.ui.status.setText("Create a cache")

    def browse_directories(self):

        dirName = QFileDialog.getExistingDirectory()
        self.ui.dirPath.setText(dirName)

    def import_movies(self):
        dirName = self.ui.dirPath.text()
        if self.clickedConnect is False :
           self.ui.status.setText("Connect to your local cache first!")
        elif len(dirName) == 0:
           self.ui.status.setText("No directory selected!")
        else :
           server.import_to_SQLMoviesTable(dirName)
           self.ui.status.setText("Movies successfully imported")


    def movie_clicked(self, item):
        """
        Changes view page to the movie information of the specific
        movie that was clicked on.
        Sets all info on the pre-made page to the given movie's info.
        """
        movie = self.ui.listWidget.itemWidget(item)
        self.ui.title.setText(movie.title)
        self.ui.year.setText(movie.year)
        self.ui.fileLoc.setText("C:/deez/nutz")
        self.ui.stackedWidget.setCurrentIndex(2)
        print(movie.title + " is clicked!!!")

if __name__ == "__main__":
    app = QApplication([])
    widget = MovieApp()
    widget.show()
    sys.exit(app.exec_())
