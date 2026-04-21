from os import getcwd

from django.db import connection

SQL_DIR = getcwd()+"/intersecter/services/files_sql/"

SQL_FILES = [
    SQL_DIR + "top_movie.sql"]


def SQL_executor(sql_file:str, **sql_params):

    with open(sql_file) as f:
        template = f.read()

    final_sql = template.format(**sql_params)
    print(final_sql)

    with connection.cursor() as cursor:
        cursor.execute(final_sql)
        #result = cursor.fetchall()
        result = cursor.fetchone() #robimy fetchone() bo i tak mamy LIMIT 1
        #fetchall() zwraca liste krotek (wierszy) [()] wiec potem w views jak robimy
        #[...,...,...] = Intersecter(...) to nie potrafi przypisac wyniku do trzech zmiennych
        #ewentualnym rozwiazaniem byloby tez wyciagniecie pierwsze elementu z wyniku Interceter(...)

    #return cursor.fetchall() - nie moze byc tutaj tego bo cursor został zamkniety po wyjsciu z with
    return result


def Intersect(users, genre, counter=0):
    users = ", ".join([f"'{u}'" for u in users]) #wartosci w "" sa traktowane w sql jako kolumny
    #trzeba bylo zamienic na ''
    genre = f"'{genre.capitalize()}'"
    #trzeba bylo dac .capitalize() bo genre bylo z malej litery a w database jest z duzej
    the_movie = SQL_executor(SQL_FILES[0], users_list=users, n=counter, selected_genre=genre)

    #sprawdzic potem !the_movie - sytuacja gdzie nic nie wyjdzie
    return the_movie
