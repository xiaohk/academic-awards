import requests
import urllib.parse
import time
import re

from bs4 import BeautifulSoup
from json import load, dump
from tqdm import tqdm


url = "https://aaai.org/about-aaai/aaai-awards/the-aaai-fellows-program/elected-aaai-fellows/"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
}

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

h2s = soup.select("h2")
people = []

for h2 in h2s:
    if "Elected" in h2.text:
        year = int(re.sub(r"Elected in (\d{4})", r"\1", h2.text))

        if year > 1991:
            siblings = h2.find_next_siblings()

            for i, sibling in enumerate(siblings):
                elements = list(sibling.children)

                person = {
                    "name": "",
                    "affiliation": "",
                    "contribution": "",
                    "year": year,
                }

                if sibling.name == "h2":
                    break

                person["name"] = elements[0].replace("\xa0", "").rstrip(",").rstrip(" ")
                person["affiliation"] = elements[1].text.replace("\xa0", "")

                if elements[2].name == "br":
                    person["contribution"] = elements[3].replace("\xa0", "")
                else:
                    person["contribution"] = elements[2].replace("\xa0", "")

                people.append(person)

        else:
            # Special parsing rules for 1991 and 1990
            sibling = h2.find_next_sibling()
            person = None

            for element in sibling.children:
                if element.name == None:
                    if person:
                        people.append(person)

                    person = {
                        "name": element.replace("\xa0", "").rstrip(",").rstrip(" "),
                        "affiliation": "",
                        "contribution": "",
                        "year": year,
                    }

                elif element.name == "em":
                    person["affiliation"] = element.text.replace("\xa0", "")

            people.append(person)

dump(people, open("data/aaai-fellows.json", "w", encoding="utf8"))
