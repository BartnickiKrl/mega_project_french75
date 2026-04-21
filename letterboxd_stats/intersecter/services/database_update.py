
import asyncio

import aiohttp

from ..models import Directors, Genres, LetterboxdUsers, Movies
from .decorator import *
from .scraper import *
from .TMDB_api import get_movie_info


@measure_time_async
async def manage_scrapping(users:list):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "deskop": "True",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://letterboxd.com/",
        }
    semaphore_web = asyncio.Semaphore(100)
    semaphore_API = asyncio.Semaphore(35)
    async with aiohttp.ClientSession(headers = headers)  as session:
        movies_info={}
        #fetch watchlists równolegle
        watchlist_tasks = [
            fetch_watchlist(session, user, semaphore_web)
            for user in users
        ]

        watchlists = await asyncio.gather(*watchlist_tasks)
        watchlists = {k: v for d in watchlists for k, v in d.items()}

        all_titles = []
        for _,titles in watchlists.items():
            all_titles.extend(titles)
        unique_titles = list(set(all_titles))

        # get movie info równolegle
        movie_tasks = [
            get_movie_info(session, title, semaphore_API)
            for title in unique_titles
        ]

        results = await asyncio.gather(*movie_tasks)
        for i in range(0, len(unique_titles)):
            movies_info[ unique_titles[i] ] = results[i]

    # uruchom osobno
    await asyncio.to_thread(save_to_database, watchlists, movies_info)

    return movies_info

@measure_time()
def save_to_database(movies_users, movies_info):

    # DODANIE WSZYSTKICH NOWYCH FILMÓW
    existing_movie_obj = {m.Title: m for m in Movies.objects.all()}
    new_movie_obj = []

    movies_info = {
        key: info for key, info in movies_info.items() if info != 'Nie znaleziono filmu.'}

    for _, info in movies_info.items():
        title = info["title"]
        year = info["year"] if info["year"].isdigit() else 1900

        if title not in existing_movie_obj:
            movie_obj = Movies(Title=title, Year=year)
            new_movie_obj.append(movie_obj)
            existing_movie_obj[title] = movie_obj

    Movies.objects.bulk_create(new_movie_obj, ignore_conflicts=True)


    #DODANIE WSZYSTKICH NOWYCH UZYTKOWNIKÓW
    existing_users_obj = {u.NickName: u for u in LetterboxdUsers.objects.all()}
    new_users_obj = []

    for nickname, _ in movies_users.items():
        user_obj = LetterboxdUsers(NickName=nickname)
        if nickname not in existing_users_obj:
            new_users_obj.append(user_obj)

    LetterboxdUsers.objects.bulk_create(new_users_obj, ignore_conflicts=True)


    #ZEBRANIE ID Z DODANYCH FILMÓW (ID USERA TO NICKNAME)
    titles_to_get = list(movies_info.keys())
    movie_id_map = dict(
        Movies.objects.filter(Title__in=titles_to_get).values_list('Title', 'id'))

    #DODANIE RELACJI MIĘDZY UŻYTKOWNIKAMI A FILMAMI
    UserMovieRelation = LetterboxdUsers.MovieID.through
    relations = []

    for nickname, titles in movies_users.items():
        for t in titles:
            m_id = movie_id_map.get(t)
            if m_id:
                relations.append(
                    UserMovieRelation(letterboxdusers_id=nickname, movies_id=m_id)
                )
    UserMovieRelation.objects.bulk_create(relations, ignore_conflicts=True)


    #DODANIE WSZYSTKICH GATUNKÓW
    genre_names = [
        "Action", "Adventure", "Animation", "Comedy", "Crime",
        "Documentary", "Drama", "Family", "Fantasy", "History",
        "Horror", "Music", "Mystery", "Romance", "Science Fiction",
        "Thriller", "TV Movie", "War", "Western"
    ]

    genre_obj = [Genres(Name=name) for name in genre_names]
    Genres.objects.bulk_create(genre_obj, ignore_conflicts=True)

    #DODANIE RELACJI MIĘDZY FILMAMI A GATUNKAMI
    GenreMovieRelation = Movies.GenreID.through
    relations = []

    for title, info in movies_info.items():
        m_id = movie_id_map.get(title)
        if m_id:
            for g_name in info.get("genres", []):
                    if g_name not in genre_names: g_name = "Drama"
                    relations.append(GenreMovieRelation(movies_id=m_id, genres_id=g_name))
    GenreMovieRelation.objects.bulk_create(relations, ignore_conflicts=True)


    #DODANIE REŻYSERÓW I RELACJI Z NIMI
    director_names = set(info["director"] for info in movies_info.values() if info.get("director"))
    director_obj = [Directors(Name=name) for name in director_names]
    Directors.objects.bulk_create(director_obj, ignore_conflicts=True)

    DirectorMovieRelation = Movies.DirectorID.through
    relations = []

    for title, info in movies_info.items():
        m_id = movie_id_map.get(title)
        if m_id:
            relations.append(
                DirectorMovieRelation(directors_id=info["director"], movies_id=m_id)
            )
    DirectorMovieRelation.objects.bulk_create(relations, ignore_conflicts=True)


# if __name__=="__main__":
#     nicknames = ["kurstboy","zoerosebryant"]
#     for i in range(4):
#         print(i+1)
#         asyncio.run(manage_scrapping(users=nicknames))
