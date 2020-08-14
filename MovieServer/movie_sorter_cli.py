import MovieServer.movie_sorter as ms
import pyodbc
import sys 
import MovieServer.constant as c

#connects to SQL Database
 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+c.SERVER+
                      ';DATABASE='+c.DATABASE+';UID='+c.USERNAME+';PWD='+ c.PASSWORD)
cursor = cnxn.cursor()


movies, movies_not_found = ms.get_movies_in_dir(sys.argv[1])
   
def export_to_SQLMoviesTable():
    for movie in movies:
        try:
            cursor.execute('''
                        INSERT INTO DB_A0C996_JMProjects.dbo.Movies 
                        (movie, rotten_tomato_score, imdb_score, metascore, runtime,
                        release_year, genre, plot, director, actors, awards, cumul_score)
                        VALUES
                        (?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (movie.name),(movie.rotten_tom_score),(movie.imdb_score),(movie.metascore),(movie.runtime),
                        (movie.release_year), (movie.genre),(movie.plot),(movie.director),(movie.actors),(movie.awards),
                        (round((movie.rotten_tom_score + movie.metascore + 10*movie.imdb_score)/3,0)))
            cnxn.commit()
        except pyodbc.IntegrityError: 
            # The Integrity Error arises when duplicates are attempted to be inserted , there is a primary key serverside which does not allow this
            # but raises an error which has to be waived to continue running the insert procedure
            pass

def adv_search( movie ,release_year, genre):
    if movie != None:
        movie = str("%"+ movie+"%" )
    elif genre != None:
        genre = str("%"+ genre+"%" )
    # the % xxx % format is syntax to allow the keyword searches to be performed
    movies_db=cursor.execute('''SELECT * FROM Movies
                    WHERE   (movie like (?) or (?) IS NULL) AND
                            (release_year = (?) or (?) IS NULL) AND
                            (genre like (?) or (?) IS NULL)
                            '''
                            ,movie, movie, release_year, release_year, genre, genre)
    for row in movies_db:
        print(row[1])

    
def apply_filters(score_option,year_option):
    
    if score_option == "TRUE":
        score_filter=int(input("Select a movie ranking metric:\n" +
              "[1] Rotten Tomatoes \n" +
              "[2] IMDB \n" +
              "[3] Metascore \n" +
              "[4] Cumulative Score (of above options)\n\n "))
        if score_filter == 1 :
            filter_option = 'rotten_tomato_score'
        elif score_filter == 2 :
            filter_option = 'imdb_score'
        elif score_filter == 3 :
            filter_option = 'metascore'
        elif score_filter == 4 :
            filter_option = 'cumul_score'
            
    elif year_option == "TRUE":
        filter_option= "release_year"
        
    ASC_DSC=int(input('Would you like your sorting option to be in ascending or descending order?\n'+
                      "[1] Ascending \n" +
                      "[2] Descending \n\n"))
    if ASC_DSC == 1:
        ASC_DSC = 'ASC'
    elif ASC_DSC == 2:
        ASC_DSC = 'DESC'
        
    movies_db = cursor.execute('''exec sp_SortData @OrderByColumnName =  ?, @ASC_DSC = ?  ''',filter_option, ASC_DSC)
    #the stored procedure invoked here can be viewed under the JMprojects database , under programmability, and stored procedures 
    #this format can be used to modularize fields which are columnnames
    
    print('')
    for row in movies_db:
        print(row[1])
 
def display_movies_not_found():
    print(c.ERROR_MSSG)
    for movie in movies_not_found:
        print(movie)

display_movies_not_found() 
export_to_SQLMoviesTable()
        
#adv_search(None,None,'comedy')   # the format is (movie,release year, genre)

apply_filters("TRUE","FALSE") # the format is (score filter , release_year filter)
#apply_filters("FALSE","TRUE")

