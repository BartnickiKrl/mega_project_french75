
import asyncio

from django.shortcuts import redirect, render

from .models import *
from .services.database_update import manage_scrapping
from .services.intersecter import Intersect
from .services.TMDB_api import get_poster


def home(request):
    if request.method == "POST":
        nicknames = request.POST.getlist('nickname[]')
        asyncio.run(manage_scrapping(users=nicknames))
        genre = request.POST.get('genre')
        print(f"{nicknames}, {genre}")

        # Zerowanie sesji
        if 'movies_already_found' in request.session:
            del request.session['movies_already_found']

        # Inicjalizacja słownika w sesji
        movies = request.session.get('movies_already_found', [])

        [title, year, director] = Intersect(nicknames, genre, movies)
        if title is None and year is None and director is None:
            return redirect('intersect-deadend')

        movies.append(title)

        # Zapis do sesji
        request.session['movies_already_found'] = movies
        request.session['last_nicknames'] = nicknames


        print(f"{nicknames}, {genre}")
        return render(request, 'intersecter/movie.html', {
            "title": title,
            "year": year,
            "director": director,
            "poster_url": get_poster(title)
        })
    return render(request, 'intersecter/home.html')

def movie(request):
    if request.method == "POST":
        genre = request.POST.get('genre')
        print(f"nowy gatunek {genre}")
        nicknames = request.session.get('last_nicknames', [])
        movies = request.session.get('movies_already_found', [])

        [title, year, director] = Intersect(nicknames, genre, movies)
        if title is None and year is None and director is None:
            return redirect('intersect-deadend')

        movies.append(title)

        # Zapis do sesji
        request.session['movies_already_found'] = movies
        request.session['last_nicknames'] = nicknames

        # Aktualizacja sesji
        request.session.modified = True


        print(f"nowy gatunek {genre}")
        return render(request, 'intersecter/movie.html', {
            "title": title,
            "year": year,
            "director": director,
            "poster_url": get_poster(title),
            "genre": genre
        })
    return render(request, 'intersecter/movie.html')


def deadend(request):
    return render(request, 'intersecter/deadend.html')


# Rozwiązanie z counterem

# def home(request):
#     if request.method == "POST":
#         nicknames = request.POST.getlist('nickname[]')
#         manage_scrapping(nicknames=nicknames)

#         genre = request.POST.get('genre')
#         print(f"{nicknames}, {genre}")

#         if genre == 'random':
#             [title, year, director, genre] = Intersect(nicknames, genre)
#         else:
#             [title, year, director] = Intersect(nicknames, genre)

#         # Inicjalizacja słownika w sesji
#         genres_counter = request.session.get('genres_counter', {})
#         genres_counter[genre] = 0

#         # Zapis do sesji
#         request.session['genres_counter'] = genres_counter
#         request.session['last_nicknames'] = nicknames

#         #[title, year, director] = Intersect(nicknames, genre)

#         print(f"{nicknames}, {genre}")
#         return render(request, 'intersecter/movie.html', {
#             "title": title,
#             "year": year,
#             "director": director,
#             "poster_url": get_poster(title)
#         })
#     return render(request, 'intersecter/home.html')

# def movie(request):
#     if request.method == "POST":
#         genre = request.POST.get('genre')
#         print(f"nowy gatunek {genre}")
#         nicknames = request.session.get('last_nicknames', [])
#         genres_counter = request.session.get('genres_counter', {})

#         if genre == 'random':
#             [title, year, director, genre] = Intersect(nicknames, genre)
#         else:
#             [title, year, director] = Intersect(nicknames, genre)

#         new_count = genres_counter.get(genre, -1) + 1
#         genres_counter[genre] = new_count

#         # Aktualizacja sesji
#         request.session['genres_counter'] = genres_counter
#         request.session.modified = True

#         [title, year, director] = Intersect(nicknames, genre, counter=new_count)

#         print(f"nowy gatunek {genre}")
#         return render(request, 'intersecter/movie.html', {
#             "title": title,
#             "year": year,
#             "director": director,
#             "poster_url": get_poster(title),
#             "genre": genre
#         })
#     return render(request, 'intersecter/movie.html')
