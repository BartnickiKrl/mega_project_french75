from parser import *
from scraper import LetterboxdClient
from TMDB_api import get_movie_info

import concurrent.futures
import requests

def update(nicnames:list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        wyniki = executor.map(LetterboxdClient.fetch_watchlist, nicnames)


if __name__=="__main__":
    main()
