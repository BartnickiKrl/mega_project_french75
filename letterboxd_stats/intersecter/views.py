from django.shortcuts import redirect, render


def home(request):
    if request.method == "POST":
        nicknames = request.POST.getlist('nickname[]')
        genre = request.POST.get('genre')

        print(f"{nicknames}, {genre}")
        return redirect('intersect-movie')
    return render(request, 'intersecter/home.html')

def movie(request):
    if request.method == "POST":
        genre = request.POST.get('genre')

        print(f"nowy gatunek {genre}")
    return render(request, 'intersecter/movie.html')
