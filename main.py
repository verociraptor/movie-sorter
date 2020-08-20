import sys
import os
from MovieServer import movie_sorter_server as server
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QListWidgetItem, QTableWidgetItem, QAbstractItemView
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MovieItem(QWidget):
    """
    Custom widget to create the list view of movies in
    the search page
    TODO: attach all other info of movie and maybe make it prettier
    """
    def __init__(self, title, rottenTom, metascore, imdbScore, year, genre,
                    plot, director, runtime, awards, actors, avgScore):
        super(MovieItem, self).__init__()
        self.init_widget(title, rottenTom, metascore, imdbScore, year, genre,
                         plot, director, runtime, awards, actors, avgScore)

    def init_widget(self, title, rottenTom, metascore, imdbScore, year, genre,
                        plot, director, runtime, awards, actors, avgScore):
        self.title = title
        self.rottenTom = rottenTom
        self.metascore = metascore
        self.imdbScore = imdbScore
        self.year = year
        self.genre = genre
        self.plot = plot
        self.director = director
        self.runtime = runtime
        self.awards = awards
        self.actors = actors
        self.avgScore = avgScore

        #display this info only in the search page
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

    def display_widget(self, ui):
        ui.title.setText(self.title)
        ui.runtime_2.setText(self.runtime)
        ui.title.setStyleSheet("font: 20pt Comic Sans MS")
        ui.year.setText(self.year)
        ui.fileLoc.setText("C:/deez/nutz")
        ui.textEdit.setHtml("<section><strong>Plot:</strong><p>" + self.plot + "</p></section><br>" +
                            "<section><strong>Director:</strong><p>" + self.director+ "</p></section><br>" +
                            "<section><strong>Actors:</strong><p>" + self.actors + "</p></section><br>" +
                            "<section><strong>Awards:</strong><p>" + self.awards + "</p></section>")
        self.set_scores_table(ui)

    def set_scores_table(self, ui):
        if(self.imdbScore != 0.0):
            ui.scoresTable.setItem(0, 0, QTableWidgetItem(self.imdbScore))
        else:
            ui.scoresTable.setItem(0, 0, QTableWidgetItem("n/a"))

        if(self.rottenTom != 0.0):
            ui.scoresTable.setItem(0, 1, QTableWidgetItem(self.rottenTom))
        else:
            ui.scoresTable.setItem(0, 1, QTableWidgetItem("n/a"))

        if(self.metascore != 0.0):
            ui.scoresTable.setItem(0, 2, QTableWidgetItem(self.metascore))
        else:
            ui.scoresTable.setItem(0, 2, QTableWidgetItem("n/a"))

        if(self.avgScore != 0.0):
            ui.scoresTable.setItem(0, 3, QTableWidgetItem(self.avgScore))
        else:
            ui.scoresTable.setItem(0, 3, QTableWidgetItem("n/a"))

        ui.textEdit.setReadOnly(True)
        ui.scoresTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        ui.scoresTable.setSelectionMode(QAbstractItemView.NoSelection)

class MovieApp(QWidget):
    """
    App widget to start the whole app.
    Sets the buttons and movie views, and
    gets the default ui made.
    """
    def __init__(self):
        super(MovieApp, self).__init__()
        self.ui = self.load_ui()
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
        self.ui.listWidget.itemClicked.connect(self.movie_clicked)


    def init_movies_view(self):
        """
        Sets up default list of movies shown in search page.
        Lists all movies in given local database.
        """
        list = server.get_all_movies(True, False) # default Ascending Alphanumerical order
        self.display_movies(list)

    def display_movies(self, list):
        for col in list:
            movie = MovieItem(col[1], str(col[2]), str(col[3]), str(col[4]),
                                str(col[5]), col[6], col[7], col[8], str(col[9]) + " min",
                                col[10], col[11], str(col[12]))
                                  # name and year and runtime
            myQListItem = QListWidgetItem(self.ui.listWidget)
            myQListItem.setSizeHint(movie.sizeHint())
            self.ui.listWidget.addItem(myQListItem)
            self.ui.listWidget.setItemWidget(myQListItem, movie)

    def update_movies_view(self):
    #TODO : fix bug where if nothing is selected or if ASC/DESC is only selected - an error is thrown pressing search
        """
        Updates movies in search page with new search queries
        """
        searchtype = None
        # for radio buttons, either one or the other will be checked
        if self.ui.avgScore.isChecked() or self.ui.releaseYear.isChecked() or self.ui.runtime.isChecked():

            searchtype = "filter"
            list = server.apply_filters_ui(self.ui.avgScore.isChecked()
                                            ,self.ui.releaseYear.isChecked()
                                            ,self.ui.runtime.isChecked()
                                            ,self.ui.ASC.isChecked()
                                            ,self.ui.DSC.isChecked())
        # keyword box has an input
        if len(self.ui.keyword.text()) != 0:
            searchtype = "keyword"
            list = server.keyword_search_ui( self.ui.keyword.text() )

        #no search option selected
        #user wants all movies whether or not asc or des is checked
        if searchtype is None:
            list = server.get_all_movies(self.ui.ASC.isChecked()
                                            ,self.ui.DSC.isChecked())

        self.ui.listWidget.clear()  #clears all movies in list
        self.display_movies(list)


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
        movie.display_widget(self.ui)
        self.ui.stackedWidget.setCurrentIndex(2)
        print(movie.title + " is clicked!!!")

if __name__ == "__main__":
    app = QApplication([])
    widget = MovieApp()
    widget.show()
    sys.exit(app.exec_())
