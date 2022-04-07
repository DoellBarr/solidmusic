from aiohttp import ClientSession
from bs4 import BeautifulSoup as Soup


async def parse_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    async with ClientSession(headers=headers) as session, session.get(url) as response:
        html = await response.text()
    return Soup(html, "html.parser")


async def get_lyrics(parsed_url: Soup):
    containers = parsed_url.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})
    lyrics = [containers[i].text for i in range(0, len(containers), 2)]
    return "".join([str(x) for x in lyrics]).strip("\n")


async def get_artist_name(parsed_url: Soup):
    containers = parsed_url.find_all("span", {"class": "BNeawe s3v9rd AP7Wnd"})
    return containers[1].text


async def get_title(page_soup: Soup):
    # containerize
    containers = page_soup.find_all("span", {"class": "BNeawe tAd8D AP7Wnd"})
    return containers[0].text
