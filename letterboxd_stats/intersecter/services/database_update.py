import concurrent.futures

from ..models import Directors, Genres, LetterboxdUsers, Movies
from .parser import get_titles, get_watchlist_len
from .scraper import LetterboxdClient
from .TMDB_api import get_movie_info


def manage_scrapping(nicknames:list):
    movies = {}
    x = []
    for user in nicknames:
        client = LetterboxdClient()
        r = client.fetch_watchlist(username=user, page=0)
        pages = get_watchlist_len(r)
        films_first = get_titles(r)
        if pages > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                responses = executor.map(client.fetch_watchlist, [user]*pages, \
                                        range(1, pages+1))
            films_titles = []
            for r in responses:
                films_titles += get_titles(r)
            movies[user] = films_first + films_titles
        else:
            movies[user] = films_first
        # print(f"len movies[user] = {len(movies[user])}")
        # print(movies[user])
        x.extend(movies[user])


    titles_for_info = list(set(x)) # tylko unikalne wartości
    movies_info = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        films_info = list(executor.map(get_movie_info, titles_for_info))
    print(films_info)
    for i in range(0, len(titles_for_info)):
        movies_info[ titles_for_info[i] ] = films_info[i]

    save_to_database(movies, movies_info)


def save_to_database(movies, movies_info):
    for nickname, film_titles in movies.items():
        user, _ = LetterboxdUsers.objects.get_or_create(NickName=nickname)

        for film_key in film_titles:
            info = movies_info.get(film_key) #szybsze niż wołanie słownika 4 razy
            if not info:
                continue

            movie, created = Movies.objects.get_or_create(
                Title=info["title"],
                Year=info["year"]
            )

            if created:
                for g_name in info.get("genres", []):
                    genre, _ = Genres.objects.get_or_create(Name=g_name)
                    movie.GenreID.add(genre)

                d_name = info.get("director")
                if d_name:
                    director, _ = Directors.objects.get_or_create(Name=d_name)
                    movie.DirectorID.add(director)

            user.MovieID.add(movie)


if __name__=="__main__":
    pass
