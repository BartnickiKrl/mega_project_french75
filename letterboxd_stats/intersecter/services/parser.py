from bs4 import BeautifulSoup

from .scraper import LetterboxdClient


def get_watchlist_len(r):
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    page_list = soup.find("div", class_="paginate-pages")
    number_of_pages = page_list.findChildren()[0].findChildren()[-1].get_text()
    return number_of_pages

def get_titles(r):
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("span", class_ = "frame-title" )
    print(soup.find("li", class_ = "griditem"))
    # print(f"len of titles: {len(titles)}")
    # for title in titles:
    #     print(title.string)





if __name__ == "__main__":

    client = LetterboxdClient()
    r = client.fetch_watchlist(username="majkelos3",page=0)
    get_watchlist_len(r)
    get_titles(r)
