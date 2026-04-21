
import asyncio

from django.shortcuts import render

from .models import *
from .services.database_update import manage_scrapping
from .services.TMDB_api import get_poster


def home(request):
    if request.method == "POST":
        nicknames = request.POST.getlist('nickname[]')
        asyncio.run(manage_scrapping(users=["kurstboy","zoerosebryant"]))
        genre = request.POST.get('genre')
        first = Movies.objects.first()

        print(f"{nicknames}, {genre}")
        return render(request, 'intersecter/movie.html', {"title": first.Title,
                                                         "year": first.Year,
                                                         "poster_url": get_poster(first.Title)})
    return render(request, 'intersecter/home.html')

def movie(request):
    if request.method == "POST":
        genre = request.POST.get('genre')
        print(f"nowy gatunek {genre}")
        second = Movies.objects.all()[1]
        return render(request, 'intersecter/movie.html', {"title": second.Title,
                                                         "year": second.Year,
                                                         "poster_url": get_poster(second.Title)})
    return render(request, 'intersecter/movie.html')
