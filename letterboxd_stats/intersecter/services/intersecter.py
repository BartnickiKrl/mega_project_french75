from os import getcwd

from django.db import connection

SQL_DIR = getcwd()+"/intersecter/services/files_sql/"

SQL_FILES = [
    SQL_DIR + "top_movie.sql"]


def SQL_executor(sql_file:str, **sql_params):

    with open(sql_file) as f:
        template = f.read()

    final_sql = template.format(**sql_params)

    with connection.cursor() as cursor:
        cursor.execute(final_sql)

    return cursor.fetchall()


def Intersect(users, genre, counter=0):
    users = ", ".join([f"'{u}'" for u in users])
    genre = f"'{genre}'"
    the_movie = SQL_executor(SQL_FILES[0], users_list=users, n=counter, selected_genre=genre)

    return the_movie
