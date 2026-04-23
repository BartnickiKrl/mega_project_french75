from bs4 import BeautifulSoup


def get_watchlist_len(html):
    soup = BeautifulSoup(html, "html.parser")
    page_list = soup.find("div", class_="paginate-pages")
    if(page_list is None): return 1
    number_of_pages = page_list.findChildren()[0].findChildren()[-1].get_text()

    return int(number_of_pages)

def get_titles(html):
    soup = BeautifulSoup(html, "html.parser")
    poster_grid = soup.find("div", class_ = "poster-grid" )
    posters = poster_grid.find_all("div", class_ = "react-component" )
    titles = [poster["data-item-full-display-name"].split(sep=" (")[0] for poster in posters]

    return titles
