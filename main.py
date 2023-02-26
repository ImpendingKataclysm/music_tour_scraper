import requests
import selectorlib
from headers import HEADERS

URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """ Scrape page source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


if __name__ == "__main__":
    print(scrape(URL))
