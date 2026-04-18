import requests

API_KEY = "f4ee279337d6012678be52531803c039"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_info(title):

    search_url = f"{BASE_URL}/search/movie"
    search_params = {"api_key": API_KEY, "query": title}
    search_res = requests.get(search_url, params=search_params).json()

    if not search_res['results']:
        return "Nie znaleziono filmu."

    movie_id = search_res['results'][0]['id']

    detail_url = f"{BASE_URL}/movie/{movie_id}"
    detail_params = {"api_key": API_KEY, "append_to_response": "credits"}
    movie = requests.get(detail_url, params=detail_params).json()

    title_full = movie['title']
    genres = [g['name'] for g in movie['genres']]

    director = next((person['name'] for person in movie['credits']['crew'] 
                     if person['job'] == 'Director'), "Nieznany")

    return {
        "tytul": title_full,
        "gatunki": genres,
        "rezyser": director }