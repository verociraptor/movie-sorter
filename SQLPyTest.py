import pyodbc 
import constant as c
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+c.SERVER+
                      ';DATABASE='+c.DATABASE+';UID='+c.USERNAME+';PWD='+ c.PASSWORD)
cursor = cnxn.cursor()

#insert
# cursor.execute('''
#                 INSERT INTO DB_A0C996_JMProjects.dbo.Movies (movie,genre)
#                 VALUES
#                 ('The Dark Knight', 'Suspense'),
#                 ('Argo','Thriller')
#                 ''')
# cnxn.commit()


# Select
# cursor.execute('SELECT * FROM DB_A0C996_JMProjects.dbo.Movies')
# for row in cursor:
#     print(row)


#update
# cursor.execute('''
#                 UPDATE DB_A0C996_JMProjects.dbo.Movies
#                 SET movie='Nemo'
#                 WHERE movie='Argo';
#                 ''')
# cnxn.commit()

#delete
# cursor.execute('''
#                 DELETE FROM DB_A0C996_JMProjects.dbo.Movies 
#                 WHERE movie='The Dark Knight' OR movie='Nemo';
#                 ''')
# cnxn.commit()
