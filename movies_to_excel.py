import xlsxwriter
import movie_sorter as ms
import sys
import re 
import constant as c 
import os

def print_usage():
    print("To use, enter directory of where the movies are stored. \nThe movies"
            + " themselves should also be directories. \nThe ideal naming format for a"
            + " movie directory is the movie name then the theatrical release year in parantheses."
            + " \nFor example, 'The.Lion.King(1994)'. The program will return any movies it cannot find.\n"
            + "Enter 'q' to quit program. \nEnter 'usage' to get usage. \nEnter directory path.")
            
def get_movies():
    print_usage()
    option = ""
    while True:
        option = input()
        if option == 'usage':
            print_usage()
        elif option == 'q':
            print("Quitting...")
            return
        else: #path is given
            if(not os.path.exists(option)):
                print(option + " does not exist.")
                continue
            movies, movies_not_found = ms.get_movies_in_dir(option)
            create_excel_sheet(option, movies)
            display_movies_not_found(movies_not_found)
            
def create_excel_sheet(directory, movies):
    directory = directory.split("\\")[1]
    workbook = xlsxwriter.Workbook('MoviesIn_' + directory + '_.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    
                
    for name in c.TITLES:
        worksheet.write(row, col, name)
        col += 1
      
    row = 1
    col = 0  
    for movie in movies:
        worksheet.write(row, col, movie.name)
        col += 1
        worksheet.write(row, col, movie.rotten_tom_score)
        col += 1
        worksheet.write(row, col, movie.imdb_score)
        col += 1
        worksheet.write(row, col, movie.metascore)
        col += 1
        worksheet.write(row, col, movie.release_year)
        col += 1
        worksheet.write(row, col, movie.genre)
        col += 1
        worksheet.write(row, col, movie.plot)
        col += 1
        worksheet.write(row, col, movie.runtime)
        col += 1
        worksheet.write(row, col, movie.director)
        col += 1
        worksheet.write(row, col, movie.actors)
        col += 1
        worksheet.write(row, col, movie.awards)
        col += 1
        worksheet.write(row, col, movie.orig_lang)
        row += 1
        col = 0
        
    workbook.close()

def display_movies_not_found(movies_not_found):
    print(c.ERROR_MSSG)
    for movie in movies_not_found:
        print(movie)
 
    
get_movies()
