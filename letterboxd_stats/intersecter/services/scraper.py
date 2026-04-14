import logging
from pathlib import Path

import cloudscraper

from ..utils.logging import get_logger

logger = get_logger(name=__name__, level=logging.DEBUG, log_dir=Path("logs"))

class LetterboxdClient:
    def __init__(self):
        self.session = cloudscraper.create_scraper()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://letterboxd.com/",
        })

    def fetch_watchlist(self, username: str):
        url = f"https://letterboxd.com/{username}/watchlist"
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"watchlist get request ended with code: {r.status_code}")
            print(r.text[:500])
            raise RuntimeError #tymczasowo jakiś błąd
        logger.debug(f"sucessful watchlist get request for user: {username}")
        return r

if __name__ == "__main__":
    client = LetterboxdClient()
    client.fetch_watchlist(username="majkelos3")



