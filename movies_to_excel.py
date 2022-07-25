import xlsxwriter
import movie_sorter as ms
import sys
import re 
import constant as c 
import os

def print_usage():
    print("To use, enter the master directory that holds directories that holds multiple movie directories."
            + "\nThe movies themselves should be directories. Errors will be thrown for those that are not.\nThe ideal naming format for a"
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
            for entry in os.scandir(option):
                subpath = os.path.join(option, entry)
                if entry.is_dir():#subdir of movies
                    movies, movies_not_found = ms.get_movies_in_dir(subpath)
                    create_excel_sheet(entry.name, movies, movies_not_found)
                    display_movies_not_found(movies_not_found)
                    print("\n")
            
def create_excel_sheet(directory, movies, movies_not_found):
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
    
    row += 1
    not_found_str = "Movies with no info found: "
    for movie in movies_not_found:
        not_found_str += movie

    worksheet.write(row, col, not_found_str)

        
    workbook.close()

def display_movies_not_found(movies_not_found):
    if len(movies_not_found)== 0: #all movies were found
        return;
    print(c.ERROR_MSSG)
    for movie in movies_not_found:
        print(movie)

#return true or false if a file given is a hidden one
#this is different for windows, or unix os
#code gotten from https://www.tutorialspoint.com/How-to-ignore-hidden-files-using-os-listdir-in-Python
# def file_is_hidden(p):
#     if os.name== 'nt':
#         attribute = win32api.GetFileAttributes(p)
#         return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
#     else:
#         return p.startswith('.') #linux-osx
        
get_movies()


