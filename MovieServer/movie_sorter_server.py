import MovieServer.movie_sorter as ms
import pyodbc

moviename=1

def Connect_to_Cloud():
    
    # connects to SQL Database stored in cloud
    # global defines local variables globally
    
    server = 'sql5053.site4now.net' 
    database = 'DB_A0C996_JMProjects' 
    username = 'DB_A0C996_JMProjects_admin' 
    password = 'Pa55word' 
    
    global cnxn 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';DATABASE='+database+';UID='+username+';PWD='+ password)
    global cursor 
    cursor = cnxn.cursor()

def Create_Local_Cache():
    
    # Creates a Local (SQL Express) Database and Table to store Movie Sorter Information
    # global defines local variables globally
    # this function also creates stored procedures serverside
    
    server = 'localhost\SQLEXPRESS'
    global cnxn
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';Trusted_Connection=yes',autocommit=True)
    cursor = cnxn.cursor()
    cursor.execute('''CREATE DATABASE Movies''')
    cnxn.commit()
    cursor.execute('''
                       USE Movies
                      CREATE TABLE Movies
                      (
                      id int identity(1,1)
                      ,movie nvarchar(250)
                      ,rotten_tomato_score float
                      ,metascore float
                      ,imdb_score float
                      ,release_year int
                      ,genre nvarchar(max)
                      ,plot nvarchar(max)
                      ,director nvarchar(max)
                      ,runtime int
                      ,awards nvarchar(max)
                      ,actors nvarchar(max)
                      ,cumul_score float
                      primary key (movie,release_year)
                      )
                      ''')
    cursor.execute('''CREATE PROCEDURE sp_SortData
                            @OrderByColumnName nvarchar(MAX),
                            @ASC_DSC nvarchar(MAX)
                      AS
                          DECLARE @SQLStatement nvarchar(max)
                          SET @SQLStatement = N'select * from Movies order by '+@OrderByColumnName+ ' ' + @ASC_DSC
                          EXEC sp_executesql @statement = @SQLStatement ''')
    cnxn.commit()
    #print("Created a Local Cache\n")

def Connect_to_Local_Cache():
    # global defines local variables globally   
    # Connects to Local SQL Database 
    
    server = 'localhost\SQLEXPRESS'
    database = 'Movies' 
    global cnxn
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+
                          ';DATABASE='+database+ ';Trusted_Connection=yes')
    
    global cursor 
    cursor = cnxn.cursor()
    #print("Connected to Local Cache\n")
    
    movies = cursor.execute('''SELECT * FROM Movies''')
    return movies
    #returns all movies in database upon connecting to DB

def Delete_Local_Cache():
    cnxn.autocommit = True
    cursor.execute('''ALTER DATABASE Movies SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                       GO
                       Drop Database Movies;''')  
    cnxn.commit()
    #print("Deleted Local Cache")

# 'D:/SSD/Movies/Two'
def export_to_SQLMoviesTable(directory):

    movies,movies_not_found = ms.get_movies_in_dir(directory)
    for movie in movies:
        try:
            cursor.execute('''
                        INSERT INTO Movies 
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

def adv_search( movie ,release_year_range, genre):
    if movie != None:
        movie = str("%"+ movie+"%" )
    elif genre != None:
        genre = str("%"+ genre+"%" )
    # the % xxx % format is syntax to allow the keyword searches to be performed
    elif release_year_range == None:
        release_year_range =[1800,2100]
    # includes all possible years in case of a null field, thereby omitting no movies
        
    movies=cursor.execute('''SELECT * FROM Movies WHERE
                            (movie like (?) or (?) IS NULL) AND
                            (release_year between (?) AND (?)) AND
                            (genre like (?) or (?) IS NULL)
                            '''
                            ,movie, movie, release_year_range[0], release_year_range[1], genre, genre)
    for row in movies:
        #returns movie names matching criteria
        print(row[moviename])

    
def apply_filters(score_option,year_option):
    
    if score_option == "TRUE":
        score_filter=int(input("Select a movie ranking metric:\n" +
              "[1] Rotten Tomatoes \n" +
              "[2] IDMB \n" +
              "[3] Metascore \n" +
              "[4] Cumulative Score (of above options)\n\n "))
        if score_filter == 1 :
            filter_option = 'rotten_tomato_score'
        elif score_filter == 2 :
            filter_option = 'idmb_score'
        elif score_filter == 3 :
            filter_option = 'metascore'
        elif score_filter == 4 :
            filter_option = 'cumul_score'
            
    elif year_option == "TRUE":
        filter_option= "release_year"
        
    ASC_DSC=int(input('Would you like your sorting option to be in ascending or descending numerical order?\n'+
                      "[1] Ascending \n" +
                      "[2] Descending \n\n"))
    if ASC_DSC == 1:
        ASC_DSC = 'ASC'
    elif ASC_DSC == 2:
        ASC_DSC = 'DESC'
        
    movies = cursor.execute('''exec sp_SortData @OrderByColumnName =  ?, @ASC_DSC = ?  ''',filter_option, ASC_DSC)
    #the stored procedure invoked here can be viewed under the JMprojects database , under programmability, and stored procedures 
    #this format can be used to modularize fields which are columnnames
    
    print('')
    for row in movies:
        #Returns movie names
        print(row[moviename])
        # can be modified to return any row

## First time user would run these three functions sequentially
## Description : Creates local Database and uploads movies in directory to them with API information , uncomment all three, run, then comment out again
#Create_Local_Cache()  
#Connect_to_Local_Cache()
#export_to_SQLMoviesTable('D:/SSD/Movies/Two') 
        
##Returning User doesn't need to create Database Again, would run these two functions if they have new movies to upload to the sorter        
##Description: Connects to Local SQL Database and uploads movies in directory to them with API information 
#Connect_to_Local_Cache()
#export_to_SQLMoviesTable('D:/SSD/Movies/Two')

## Alternative testing connection which doesnt need to be created anew since it'll alway be there for anyone developer to use
## Description : Connects to Cloud SQL Database and uploads movies in directory to them with API information 
#Connect_to_Cloud()
#export_to_SQLMoviesTable('D:\Movies\Test')

## A Returning User with no new movies to upload would run one of these functions to connect amd then run a filter function (lines 187 - 189)
## Description : Choose to either connect to cloud OR Local Cache but not both
#Connect_to_Cloud()
#Connect_to_Local_Cache() 
         
## Try out the Filters one by one by uncommenting, remember to connect to either the cloud or the local cache first tho
#adv_search(None,(2000,2020),None)   ## the format is (movie, release year range, genre)
#apply_filters("TRUE","FALSE") # the format is (score filter , release_year filter)
#apply_filters("FALSE","TRUE")

## Description: Deletes your local Movie Cache
# Connect_to_Local_Cache()
# Delete_Local_Cache() ## Still Buggy, best to manually delete
        

