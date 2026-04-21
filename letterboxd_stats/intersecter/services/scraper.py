import asyncio
import logging
from pathlib import Path

from ..utils.logging import get_logger
from .parser import get_titles, get_watchlist_len

BASE_URL = "https://letterboxd.com/"

logger = get_logger(name=__name__, level=logging.DEBUG, log_dir=Path("logs"))


async def fetch(session, url, semaphore):
    async with semaphore, session.get(url) as r:
        return await r.text()

# returns list of all movies from user's watchlist
async def fetch_watchlist(session, user: str,semaphore):
        url = BASE_URL + user.lower() + r"/watchlist/"
        async with semaphore, session.get(url) as resp:
            first_page = await resp.text()

        pages = get_watchlist_len(first_page)
        movies = get_titles(first_page)

        tasks = [fetch(session, f"{BASE_URL}{user}/watchlist/page/{p}/", semaphore) for p in range(2, pages + 1)]

        responses = await asyncio.gather(*tasks)
        for response in responses:
            titles_on_page = get_titles(response)
            if(titles_on_page): movies.extend(titles_on_page)

        return {user:movies}

# class LetterboxdClient:
#     BASE_URL = "https://letterboxd.com/"
#     # __instances_count = 0
#     def __init__(self):
#         self.session = cloudscraper.create_scraper()
#         self.session.headers.update({
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.9",
#             "deskop": "True",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Connection": "keep-alive",
#             "Referer": "https://letterboxd.com/",
#         })
#         # LetterboxdClient.__instances_count += 1
#     #@measure_time("ms")
#     def fetch_watchlist(self, username: str,page: int,retries = 3):
#         for i in range(retries):
#             url = self.BASE_URL + username.lower() + r"/watchlist/"
#             if page > 0:
#                 url += f"page/{page}/"
#             r = self.session.get(url)
#             if r.status_code == 200:
#                 logger.debug(f"sucessful watchlist {page} get request for user: {username}")
#                 return r
#             logger.error(f"watchlist page {page} get request ended with code: {r.status_code} for user: {username} link: {url}")
#         return r

#     def fetch_film(self,title: str):
#         url = self.BASE_URL + title
#         # r = self.session.get(url)
#         r = requests.get(url,headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#         })

#         if r.status_code != 200:
#             logger.error(f"film get request ended with code: {r.status_code} for movie: {title}")
#             # raise RuntimeError #Zrobić lepszą obsługę wyjątków i klase wyj
#         logger.debug(f"sucessful film get request for film: {title}")
#         return r








