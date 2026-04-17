from django.shortcuts import render


def home(request):
    if request.method == "POST":
        nicknames = request.POST.getlist('nickname[]')
        genre = request.POST.get('genre')

        print(f"{nicknames}, {genre}")
        return render(request, 'intersecter/movie.html', {"title": "Poor Things",
                                                         "year": "2023"})
    return render(request, 'intersecter/home.html')

def movie(request):
    if request.method == "POST":
        genre = request.POST.get('genre')
        print(f"nowy gatunek {genre}")
        return render(request, 'intersecter/movie.html', {"title": "Michael Jackson",
                                                           "year": "2026"})
    return render(request, 'intersecter/movie.html')
