import os
import requests

#Info to make API requests
OMDB_KEY = '905fe09c'
URL = 'http://www.omdbapi.com/'

class Movie:
    def __init__(self, name):
        self.name = name
        self.rotten_tom_score = 0
        self.imdb_score = 0
        self.metascore = 0
        self.release_year = 0
        self.genre = ""
        self.plot = ""
        self.runtime = 0
        self.director = ""
        self.actors = ""
        self.awards = ""
        
        
    def set_properties(self, json_resp):
        for dict_item in json_resp['Ratings']:
            if dict_item['Source'] == 'Rotten Tomatoes':
                #Takes off percentage symbol from the rotten tomatoes' value
                self.rotten_tom_score = int(dict_item['Value'].split('%')[0])
                break
        
        self.metascore = int(json_resp['Metascore']) if not is_valid(json_resp['Metascore']) else 0
        self.imdb_score = float(json_resp['imdbRating']) if not is_valid(json_resp['Metascore']) else 0
        self.release_year = int(json_resp['Year']) if not is_valid(json_resp['Metascore']) else 0
        self.genre = json_resp['Genre'] if not is_valid(json_resp['Metascore']) else "Genre not found"
        self.plot = json_resp['Plot'] if not is_valid(json_resp['Metascore']) else "Plot not found"
        self.runtime = int(json_resp['Runtime'].split(' ')[0]) if not is_valid(json_resp['Metascore']) else 0
        self.director = json_resp['Director'] if not is_valid(json_resp['Metascore']) else "Director not found"
        self.actors = json_resp['Actors'] if not is_valid(json_resp['Metascore']) else "Actors not found"
        self.awards = json_resp['Awards'] if not is_valid(json_resp['Metascore']) else "Awards not found"
           
#Todo: might have to update string parser to handle more unique cases       
def get_name(nm):
    return nm.split('(')[0].replace('.', ' ') 
    

def is_valid(string):
    return string == 'N/A'
    
def get_movies_in_dir(path):
    movies_arr = []
    for entry in os.scandir(path):
        if entry.is_dir():
            movie_name = get_name(entry.name)
            curr_movie = Movie(movie_name)
            payload = {'t': movie_name, 'apikey': OMDB_KEY}
            resp = requests.get(URL, params = payload)
            resp_json = resp.json()
            if resp:
                curr_movie.set_properties(resp_json)
                movies_arr.append(curr_movie)
    return movies_arr    
              

