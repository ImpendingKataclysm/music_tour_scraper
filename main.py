import requests
import selectorlib
import time
import sqlite3
from headers import HEADERS
from send_email import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
tour_file = "tours.txt"
connection = sqlite3.connect("tour_data.db")


def scrape(url):
    """ Scrape page source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    """ Extract specified element from page source code"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def get_row(data):
    """ Converts a string of comma separated data into a list of strings with
    no surrounding whitespace"""
    row = data.split(",")
    row = [item.strip() for item in row]
    return row


def store(extracted_data):
    """ Add new event to tour database"""
    row = get_row(extracted_data)
    print(row)
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO events VALUES(?,?,?)", (row, ))
    connection.commit()


def read(extracted_data):
    """ Query tour database to find the specified event """
    band, city, date = get_row(extracted_data)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted.lower() != "no upcoming tours":
            content = read(extracted)
            print(content)
            if not content:
                store(extracted)
                message = f"""\
                New event found!
                
                {extracted}
                """
                send_email(message=message)
        time.sleep(2)
