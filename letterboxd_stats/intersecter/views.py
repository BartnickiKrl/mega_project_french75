from django.shortcuts import render


def home(request):
    if request.method == "POST":
        nicknames = request.POST.getlist('nickname[]')
        genre = request.POST.get('genre')

        print(f"{nicknames}, {genre}")
    return render(request, 'intersecter/home.html')
