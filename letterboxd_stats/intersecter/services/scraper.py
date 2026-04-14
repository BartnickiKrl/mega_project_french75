import logging
from pathlib import Path

import requests

from ..utils.logging import get_logger

logger = get_logger(name=__name__, level=logging.DEBUG, log_dir=Path("logs"))

class LetterboxdClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
        })

    def fetch_watchlist(self, username: str):
        url = f"https://letterboxd.com/{username}/watchlist"
        r = self.session.get(url)
        if r.status_code != 200:
            logger.error(f"watchlist get request ended with code: {r.status_code}")
            raise RuntimeError #tymczasowo jakiś błąd
        logger.debug(f"sucessful watchlist get request for user: {username}")
        return r

client = LetterboxdClient()
client.fetch_watchlist(username="majkelos3")



