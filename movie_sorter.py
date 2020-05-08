import os
import requests
import re 
import constant



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
    movie_and_year = re.split('[(;)]', nm)
    movie_and_year[0] = movie_and_year[0].replace(".", " ")
    return movie_and_year

#check if movie property is available in OMDB API
def is_valid(string):
    return string != 'N/A'

#TODO: handle error cases, i.e multiple results, no results
def get_tmdb_id(nm, year):
    payload = {'api_key': constant.TMDB_KEY, 'query': nm, 'page': '1', 
                'include_adult': 'false', 'primary_release_year': year}
    resp = requests.get(constant.TMDB_URL + 'search/movie', params = payload)
    resp_json = resp.json()
    return resp_json['results'][0]['id']
 
 
def get_movie_tmdb(tmdb_id):
    payload = {'api_key': constant.TMDB_KEY}
    resp = requests.get(constant.TMDB_URL + 'movie/' + str(tmdb_id), params = payload)
    return resp.json()

#returns the ratings in an array of dictionaries 
def get_movie_omdb(imdb_id):
    payload = {'i': imdb_id, 'apikey': constant.OMDB_KEY}
    resp = requests.get(constant.OMDB_URL, params = payload)
    return resp.json()
 
#TODO: handle errors for OMDB  
def get_movies_in_dir(path):
    movies_arr = []
    for entry in os.scandir(path):
        if entry.is_dir():
            #get current movie 
            movie_year = get_name_and_year(entry.name)
            curr_movie = Movie(movie_year[0], int(movie_year[1]))
            
            #get TMDB id from TMDB
            tmdb_id = get_tmdb_id(movie_year[0], movie_year[1])
            
            #get movie info and imdb id from TMDB
            tmdb_json = get_movie_tmdb(tmdb_id)
            
            #get movie info from OMDB not seen in TMDB
            omdb_json = get_movie_omdb(tmdb_json["imdb_id"])
            
            curr_movie.set_properties(tmdb_json, omdb_json)
            movies_arr.append(curr_movie)
            
    return movies_arr    
