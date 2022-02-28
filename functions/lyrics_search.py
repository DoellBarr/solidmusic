from urllib.request import urlopen as u_reqs, Request
from bs4 import BeautifulSoup as Soup


def parse_url(url: str):
    # read url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
    }
    req = Request(url, headers=headers)
    u_client = u_reqs(req)

    page_html = u_client.read()
    u_client.close()

    return Soup(page_html, "html.parser")


def get_lyrics(page_soup: Soup):
    # containerize
    containers = page_soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})
    lyrics = [containers[i].text for i in range(0, len(containers), 2)]

    return "".join([str(x) for x in lyrics]).strip("\n")


def get_artist(page_soup: Soup):
    # containerize
    containers = page_soup.find_all("span", {"class": "BNeawe s3v9rd AP7Wnd"})
    return containers[1].text


def get_title(page_soup: Soup):
    # containerize
    containers = page_soup.find_all("span", {"class": "BNeawe tAd8D AP7Wnd"})
    return containers[0].text
