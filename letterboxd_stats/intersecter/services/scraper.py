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
