
import requests

API_KEY = "f4ee279337d6012678be52531803c039"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

async def get_movie_info(session, title, semaphore):

    search_url = f"{BASE_URL}/search/movie"
    search_params = {"api_key": API_KEY, "query": title}

    async with semaphore, session.get(search_url, params=search_params) as resp:
        search_res = await resp.json()

    # search_res = requests.get(search_url, params=search_params).json()

    if not search_res['results']:
        return "Nie znaleziono filmu."

    movie_id = search_res['results'][0]['id']
    detail_url = f"{BASE_URL}/movie/{movie_id}"
    detail_params = {"api_key": API_KEY, "append_to_response": "credits"}
    async with semaphore, session.get(detail_url, params=detail_params) as resp:
        movie = await resp.json()


    # movie = requests.get(detail_url, params=detail_params).json()

    title_full = movie['title']
    genres = [g['name'] for g in movie['genres']]
    year = movie['release_date'][:4] if movie['release_date'] else "N/A"

    director = next((person['name'] for person in movie['credits']['crew']
                     if person['job'] == 'Director'), "Nieznany")

    return {
        "title": title_full,
        "year": year,
        "genres": genres,
        "director": director
    }

def get_poster(title):
    search_url = f"{BASE_URL}/search/movie"
    search_params = {"api_key": API_KEY, "query": title}
    search_res = requests.get(search_url, params=search_params).json()
    movie_data = search_res['results'][0]
    poster_path = movie_data.get('poster_path')
    return f"{IMAGE_BASE_URL}/{poster_path}"
