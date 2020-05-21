import os
import requests
import re 
import constant as c

class Movie:
    def __init__(self, name, year):
        self.name = name
        self.tmdb_id = 0
        self.imdb_id = 0
        self.rotten_tom_score = 0
        self.imdb_score = 0
        self.metascore = 0
        self.release_year = year
        self.genre = ""
        self.plot = ""
        self.runtime = 0
        self.director = ""
        self.actors = ""
        self.awards = ""
        self.watched = False
        
   
    def set_properties(self, tmdb_info, omdb_info):
        for dict_item in omdb_info['Ratings']:
            if dict_item['Source'] == 'Rotten Tomatoes':
                #Takes off percentage symbol from the rotten tomatoes' value
                self.rotten_tom_score = int(dict_item['Value'].split('%')[0])
                break
        
        self.metascore = int(omdb_info['Metascore']) if is_valid(omdb_info['Metascore']) else 0
        self.imdb_score = float(omdb_info['imdbRating']) if is_valid(omdb_info['imdbRating']) else 0
        self.genre = omdb_info['Genre'] if is_valid(omdb_info['Genre']) else "Genre not found"
        self.plot = tmdb_info['overview'] if not None else "Plot not found"
        self.runtime = tmdb_info['runtime'] if not None else 0
        self.director = omdb_info['Director'] if is_valid(omdb_info['Director']) else "Director not found"
        self.actors = omdb_info['Actors'] if is_valid(omdb_info['Actors']) else "Actors not found"
        self.awards = omdb_info['Awards'] if is_valid(omdb_info['Awards']) else "Awards not found"
           
#movie name is in first index
#release year is in second index       
def get_name_and_year(nm):
    i = 0
    year = 0
    split_idx = 0
    #get last year seen in string name
    while(i < len(nm)):
        total = 0
        while(i < len(nm) and str.isdigit(nm[i])):
            total *= 10
            total += int(nm[i])
            i += 1
        if(total <= c.CURR_YEAR and total >= c.FIRST_MOVIE_YEAR):
            year = total
            split_idx = (i - 5)
            continue
        i += 1
    #case 1 - no '(' exists b/w movie & year  
    #case 2 - no year found in string
    movie = nm[:split_idx] if split_idx != 0 else nm  
    
    #case 3 - '(' exists regardless if year found or not
    movie_1 = re.split('[(]', movie)[0].replace(".", " ") 
    movie_and_year = [movie_1, year]
    return movie_and_year

#check if movie property is available in OMDB API
def is_valid(string):
    return string != 'N/A'

#returns movie id within tmdb in order to 
#later retrieve the imdb id
def get_tmdb_id(nm, year):
    payload = ({'api_key': c.TMDB_KEY, 'query': nm, 'page': '1', 
                'include_adult': 'false', 'primary_release_year': year}
                if year != 0 else
                {'api_key': c.TMDB_KEY, 'query': nm, 'page': '1', 
                'include_adult': 'false'})
    resp = requests.get(c.TMDB_URL + 'search/movie', params = payload)
    
    if resp.status_code != c.OK_STATUS:
        return c.error
        
    resp_json = resp.json()
    #throw error when there are multiple results if year is not given 
    tmdb_id = (resp_json['results'][0]['id'] 
                if year != 0 or resp_json['total_results'] == 1 else
                c.ERROR)
    return tmdb_id
 
#returns tmdb details of movie including the imdb id
def get_movie_tmdb(tmdb_id):
    payload = {'api_key': c.TMDB_KEY}
    resp = requests.get(c.TMDB_URL + 'movie/' + str(tmdb_id), 
                            params = payload)
                  
    if resp.status_code != c.OK_STATUS: #movie not found
        return c.ERROR 
        
    return resp.json()

#returns the omdb details of movie including the ratings
def get_movie_omdb(imdb_id):
    payload = {'i': str(imdb_id), 'apikey': c.OMDB_KEY}
    resp = requests.get(c.OMDB_URL, params = payload)
    if resp.status_code != c.OK_STATUS or not resp.json()["Response"]: #movie not found
        return c.ERROR
    
    return resp.json()
  
def get_movies_in_dir(path):
    movies_found = []
    movies_not_found = []
    for entry in os.scandir(path):
        if entry.is_dir():
            #get current movie 
            movie_year = get_name_and_year(entry.name)
            
            curr_movie = Movie(movie_year[0], int(movie_year[1]))
            #get TMDB id from TMDB
            tmdb_id = get_tmdb_id(movie_year[0], movie_year[1])
            
            if(tmdb_id != c.ERROR):
                #get movie info and imdb id from TMDB
                tmdb_json = get_movie_tmdb(tmdb_id)
                
                #get movie info from OMDB not seen in TMDB
                omdb_json = get_movie_omdb(tmdb_json["imdb_id"])
                
                if(tmdb_json != c.ERROR and omdb_json != c.ERROR):
                    curr_movie.set_properties(tmdb_json, omdb_json)
                    movies_found.append(curr_movie)
                else:
                    movies_not_found.append(entry.name)
            else:
                movies_not_found.append(entry.name)
            
    return movies_found, movies_not_found