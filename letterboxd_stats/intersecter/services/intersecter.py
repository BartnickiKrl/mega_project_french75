from os import getcwd

from django.db import connection

from .decorator import measure_time

SQL_DIR = getcwd()+"/intersecter/services/files_sql/"

SQL_FILES = [
    SQL_DIR + "top_movie.sql",
    SQL_DIR + "random.sql"]



def SQL_executor(sql_file:str, params:list):

    with open(sql_file) as f:
        template = f.read()

    u_placeholders = ", ".join(["%s"] * len(params[0]))
    m_placeholders = "' '" if not params[1] else ", ".join(["%s"] * len(params[1]))

    # Wstrzykujemy TYLKO placeholdery (bezpieczne, to nie są dane)
    query = template.format(
        u_placeholders=u_placeholders,
        m_placeholders=m_placeholders
    )

    # Przygotowujemy płaską listę parametrów dla cursor.execute
    # Kolejność musi być taka sama jak w SQL: users, potem movies, potem genre
    sql_params = [p for param in params for p in param]


    with connection.cursor() as cursor:
        cursor.execute(query, sql_params)

        result = cursor.fetchone() #robimy fetchone() bo i tak mamy LIMIT 1

    #return cursor.fetchall() - nie moze byc tutaj tego bo cursor został zamkniety po wyjsciu z with
    return result

#result = cursor.fetchall()
        #fetchall() zwraca liste krotek (wierszy) [()] wiec potem w views jak robimy
        #[...,...,...] = Intersecter(...) to nie potrafi przypisac wyniku do trzech zmiennych
        #ewentualnym rozwiazaniem byloby tez wyciagniecie pierwsze elementu z wyniku Interceter(...)


@measure_time()
def Intersect(users, genre, movies=[]):

    if genre == 'random':
        the_movie = SQL_executor(SQL_FILES[1], [users, movies])
        if the_movie is None:
            return [None,None,None]
    else:
        the_movie = SQL_executor(SQL_FILES[0], [users, movies, [genre]])
        if the_movie is None:
            the_movie = Intersect(users, 'random', movies)

    #sprawdzic potem !the_movie - sytuacja gdzie nic nie wyjdzie
    return the_movie


# users = ", ".join([f"'{u}'" for u in users]) #wartosci w "" sa traktowane w sql jako kolumny
# #trzeba bylo zamienic na ''
# genre = f"'{genre}'"
# movies= ", ".join([f"'{m}'" for m in movies])

#trzeba bylo dac .capitalize() bo genre bylo z malej litery a w database jest z duzej - zmiana
#tego w html
