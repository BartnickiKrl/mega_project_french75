from bs4 import BeautifulSoup

from .scraper import LetterboxdClient


def get_watchlist_len(r):
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    page_list = soup.find("div", class_="paginate-pages")
    number_of_pages = page_list.findChildren()[0].findChildren()[-1].get_text()
    return int(number_of_pages)

def get_titles(r):
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    poster_grid = soup.find("div", class_ = "poster-grid" )
    posters = poster_grid.find_all("div", class_ = "react-component" )
    titles = [poster["data-item-full-display-name"] for poster in posters]

    return titles
def get_image(r,title:str):
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    poster_grid = soup.find("div", class_ = "poster-grid" )
    for poster in poster_grid:
        poster["data-item-full-display-name"]












if __name__ == "__main__":

    client = LetterboxdClient()
    r = client.fetch_watchlist(username="majkelos3",page=0)
    get_watchlist_len(r)
    get_titles(r)
