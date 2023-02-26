import requests
import selectorlib
import time
from headers import HEADERS
from send_email import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
tour_file = "tours.txt"


def scrape(url):
    """ Scrape page source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted_data):
    with open(tour_file, "a") as file:
        file.write(extracted_data + "\n")


def read(extracted_data):
    with open(tour_file, "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)
        if extracted.lower() != "no upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="New event found!")
        time.sleep(2)
