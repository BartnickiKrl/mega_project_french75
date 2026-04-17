import logging
from pathlib import Path

import cloudscraper

from ..utils.logging import get_logger
from .decorator import measure_time

logger = get_logger(name=__name__, level=logging.DEBUG, log_dir=Path("logs"))

class LetterboxdClient:
    BASE_URL = "https://letterboxd.com/"
    # __instances_count = 0
    def __init__(self):
        self.session = cloudscraper.create_scraper()
        self.last_status_code = 200
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "deskop": "True",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://letterboxd.com/",
        })
        # LetterboxdClient.__instances_count += 1
    #@measure_time("ms")
    def fetch_watchlist(self, username: str,retries = 3):
        url = self.BASE_URL + username
        r = self.session.get(url)
        self.last_status_code = r.status_code
        if self.last_status_code != 200:
            logger.error(f"watchlist get request ended with code: {r.status_code} for user: {username}")
            # raise RuntimeError #Zrobić lepszą obsługę wyjątków i klase wyj
        logger.debug(f"sucessful watchlist get request for user: {username}")
        return r

    #@measure_time("ms")
    def fetch_film(self,title: str,retries = 2):
        url = self.BASE_URL + title
        r = self.session.get(url)
        self.last_status_code = r.status_code
        if self.last_status_code != 200:
            logger.error(f"film get request ended with code: {r.status_code} for movie: {title}")
            # raise RuntimeError #Zrobić lepszą obsługę wyjątków i klase wyj
        logger.debug(f"sucessful film get request for film: {title}")
        return r
    def reset_status_code(self):
        self.last_status_code = 200


    #cast jest w basehtml URL



if __name__ == "__main__":

    film_requests_test = [
        "/film/grave-of-the-fireflies/",
        "/film/parasite/",
        "/film/interstellar/",
        "/film/fight-club/",
        "/film/inception/",
        "/film/the-godfather/",
        "/film/the-godfather-part-ii/",
        "/film/pulp-fiction/",
        "/film/the-dark-knight/",
        "/film/forrest-gump/",
        "/film/shutter-island/",
        "/film/the-matrix/",
        "/film/se7en/",
        "/film/whiplash/",
        "/film/parasite-2019/",  # czasem alternatywne slugi
        "/film/dune-2021/",
        "/film/dune-part-two/",
        "/film/spirited-away/",
        "/film/your-name/",
        "/film/oldboy/",
        "/film/american-psycho/",
        "/film/whiplash/",
        "/film/its-a-wonderful-life/",
        "/film/whiplash/",  # celowo duplikat
        "/film/the-social-network/",
        "/film/gladiator/",
        "/film/whiplash/",
        "/film/joker/",
    ]

    print(f"{len(film_requests_test)}")

    @measure_time()
    def test_funtion():
        client = LetterboxdClient()
        client.fetch_watchlist(username="majkelos3")
        MAX_WORKERS = 5

        for film in film_requests_test:
            client.fetch_film(title = film)
            if(client.last_status_code != 200):
                client.reset_status_code()
                client_N = LetterboxdClient()
                client_N.fetch_film(title=film)
            # time.sleep(0.5)
test_funtion()





