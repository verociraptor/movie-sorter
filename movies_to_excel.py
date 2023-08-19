import xlsxwriter
import movie_sorter as ms
import constant as c 
import os

def print_usage():
    print("---------------------------------------------- \nTo use, enter the master directory that holds directories that holds multiple movie directories."
            + "\nThe movies themselves should be directories. Errors will be thrown for those that are not.\nThe ideal naming format for a"
            + " movie directory is the movie name then the theatrical release year in parantheses."
            + " \nFor example, 'The.Lion.King(1994)'. The program will return any movies it cannot find.\n"
            + "Enter 'q' to quit program. \nEnter 'usage' to get usage. \nEnter full directory path without quotes, e.g. 'D:\\path\\to\\root\\dir\\of\\movies'.\n"
            + "----------------------------------------------")

def run():
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

            get_movies(option)

def get_movies(directory_name):
    excel_name = get_excel_name()

    print("Reading movies in directory " + directory_name + " ...")
    movies, movies_not_found = ms.get_movies_in_dir(directory_name)

    if len(movies) == 0:
        print("No movies found to add into excel sheet. Please try again.")
        return

    print("Creating movie excel at path " + excel_name + " ...")
    create_excel_sheet(excel_name, movies, movies_not_found)
    display_movies_not_found(movies_not_found)

    print("Movie excel has been created. Exit or provide another directory.")

def get_excel_name():
    while True:
        print("Provide full path, including the name and extension, for this movie excel sheet without quotes (e.g. 'D:\\full\\path\\to\\my\\movie_excel.xlsx'):")
        name = input().strip()
        if name == "" or name is None:
            continue
        else:
            return name

def create_excel_sheet(file_name, movies, movies_not_found):
    workbook = xlsxwriter.Workbook(file_name)
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
    not_found_str = "Movies with no info found:\n"
    for movie in movies_not_found:
        not_found_str += movie

    worksheet.write(row, col, not_found_str)
    workbook.close()

def display_movies_not_found(movies_not_found):
    if len(movies_not_found)== 0: #all movies were found
        return
    print(c.ERROR_MSSG)
    for movie in movies_not_found:
        print(movie)

run()