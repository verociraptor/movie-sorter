import movie_sorter
import sys

movies = movie_sorter.get_movies_in_dir(sys.argv[1])

def get_most_recent_movie():
    list.sort(movies, key=lambda movie: movie.release_year)
    year = movies[len(movies)-1].release_year
    
    #gets all movies with same release_year if also recent
    recent_movies = [movie for movie in reversed(movies) 
                        if movie.release_year == year]
    if len(recent_movies) > 1:  
        print("Movies made most recently are:\n")
        for movie in recent_movies:
            print(movie.name + " made in " + str(movie.release_year) + "\n")
    else:
        print("Movie made most recently is: " + recent_movies[0].name
                + " made in " + str(recent_movies[0].release_year))

def get_highest_metascored_movie():
    list.sort(movies, key=lambda movie: movie.metascore)
    score = movies[len(movies)-1].metascore
    
    #gets all movies with same release_year if also recent
    metascored_movies = [movie for movie in reversed(movies) 
                        if movie.metascore == score]
    if len(metascored_movies) > 1:  
        print("Movies with the highest Metascore are:\n")
        for movie in metascored_movies:
            print(movie.name + " of rating " + str(movie.metascore) + "/100\n")
    else:
        print("Movie with the highest Metascore is: " + metascored_movies[0].name
                + " of rating " + str(metascored_movies[0].metascore) + "/100")
    
def get_shortest_runtime_movie():
    list.sort(movies, key=lambda movie: movie.runtime)
    runtime = movies[0].runtime
    
    #gets all movies with same release_year if also recent
    shortest_movies = [movie for movie in movies
                        if movie.runtime == runtime]
    if len(shortest_movies) > 1:  
        print("Movies with the shortest runtime are:\n")
        for movie in shortest_movies:
            print(movie.name + " is " + str(movie.runtime) + " min\n")
    else:
        print("Movie with the shortest runtime is: " + shortest_movies[0].name
                + " is " + str(shortest_movies[0].runtime) + " min")

def get_highest_imdbscored_movie():
    list.sort(movies, key=lambda movie: movie.imdb_score)
    score = movies[len(movies)-1].imdb_score
    
    #gets all movies with same release_year if also recent
    imdbscored_movies = [movie for movie in reversed(movies) 
                        if movie.imdb_score == score]
    if len(imdbscored_movies) > 1:  
        print("Movies with the highest IMDB score are:\n")
        for movie in imdbscored_movies:
            print(movie.name + " of rating " + str(movie.imdb_score) + "/10\n")
    else:
        print("Movie with the highest IMDB score is: " + imdbscored_movies[0].name
                + " of rating " + str(imdbscored_movies[0].imdb_score) + "/10")

def get_highest_rottentomscored_movie():
    list.sort(movies, key=lambda movie: movie.rotten_tom_score)
    score = movies[len(movies)-1].rotten_tom_score
    
    #gets all movies with same release_year if also recent
    rottenscored_movies = [movie for movie in reversed(movies) 
                            if movie.rotten_tom_score == score]
    if len(rottenscored_movies) > 1:  
        print("Movies with the highest Rotten Tomato scores are:\n")
        for movie in rottenscored_movies:
            print(movie.name + " is " + str(movie.rotten_tom_score) + "%\n")
    else:
        print("Movie with the highest Rotten Tomato score is: " 
                + rottenscored_movies[0].name + " of rating " 
                + str(rottenscored_movies[0].rotten_tom_score) + "%")
    
def display_all_movies():
    for movie in movies:
        print(movie.name + " RT: " + str(movie.rotten_tom_score)
                + " & imdb: " + str(movie.imdb_score)
                + " & metascore: " + str(movie.metascore)
                + " & runtime: " + str(movie.runtime)
                + " & release year: " + str(movie.release_year) + "\n")
        
display_all_movies()