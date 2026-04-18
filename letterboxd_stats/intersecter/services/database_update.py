import concurrent.futures

from models import Directors, Genres, LetterboxdUsers, Movies
from parser import get_titles, get_watchlist_len
from scraper import LetterboxdClient
from TMDB_api import get_movie_info


def manage_scrapping(nicknames:list):
    movies = {}
    x = []
    for user in nicknames:
        r = LetterboxdClient.fetch_watchlist(user, 0)
        pages = get_watchlist_len(r)
        films_first = get_titles(r)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            films_titles = get_titles(r for r in executor.map(LetterboxdClient.fetch_watchlist, [user]*pages, range(1, pages+1)))
        movies[user] = films_first + films_titles
        x.extend(movies[user])

    titles_for_info = set(x) # tylko unikalne wartości
    movies_info = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        films_info = executor.map(get_movie_info, titles_for_info)

    for i in range(0, len(titles_for_info)):
        movies_info[ titles_for_info[i] ] = films_info[i]



def save_to_database(movies, movies_info):
    for nickname in movies.key():
        user, _ = LetterboxdUsers.objects.get_or_create(NickName=nickname)

        for film in movies[nickname]:
            movie, exists = Movies.objects.get_or_create(
                Title=movies_info[film]["title"],
                Year=movies_info[film]["year"]
            )

            if not exists:
                for g_name in movies_info[film]["genres"]:
                    genre, _ = Genres.objects.get_or_create(Name=g_name)
                    movie.GenreID.add(genre) # add() od razu zapisuje powiązanie w tabeli pośredniej

                director_name = movies_info[film]["director"]
                director, _ = Directors.objects.get_or_create(Name=director_name)
                movie.DirectorID.add(director)

        user.MovieID.add(movie)

if __name__=="__main__":
    pass
