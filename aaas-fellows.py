import requests
import urllib.parse
import time
import re

from bs4 import BeautifulSoup
from json import load, dump
from tqdm import tqdm


def scrape_aaas_fellows(page_num):
    url = f"https://www.aaas.org/fellows/listing?page={page_num}"
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")

    people = []

    if not soup.select("tbody"):
        return people

    tags = soup.find("tbody").find_all("tr")

    for tag in tags:
        tds = tag.find_all("td")

        name = (
            tds[0]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )
        # Swap the first/last name order
        parts = name.split(", ")
        name_swapped = parts[1] + " " + parts[0]

        year = (
            tds[1]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )
        state = (
            tds[2]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )
        country = (
            tds[3]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )
        primary = (
            tds[4]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )
        affiliation = (
            tds[5]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
            .rstrip(" ")
        )

        person = {
            "name": name_swapped,
            "year": year,
            "state": state,
            "country": country,
            "primary": primary,
            "affiliation": affiliation,
        }

        people.append(person)

    return people


all_fellows = []
error_pages = []

session = requests.Session()

for p in tqdm(range(1, 500)):
    try:
        cur_fellows = scrape_aaas_fellows(p)
        all_fellows.extend(cur_fellows)

        if len(cur_fellows) == 0:
            error_pages.append(p)
            print("No author on page ", p)
            break

    except:
        print("Error on page ", p)
        error_pages.append(p)
        continue

    if p % 100 == 0:
        dump(all_fellows, open("data/aaas-fellows.json", "w", encoding="utf8"))

dump(all_fellows, open("data/aaas-fellows.json", "w", encoding="utf8"))
