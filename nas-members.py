import requests
import urllib.parse
import time
import re

from bs4 import BeautifulSoup
from json import load, dump
from tqdm import tqdm


url = "https://www.nasonline.org/member-directory/living-member-list.html"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
}

response = requests.get(url, headers=header, timeout=600)
soup = BeautifulSoup(response.text, "html.parser")

tags = soup.select("div.entry")
members = []

for tag in tags:
    name = tag.find("a").text

    person = {
        "name": name,
        "year": "",
        "affiliation": "",
        "primary": "",
        "secondary": "",
    }

    try:
        if tag.select("span.membership-type"):
            year_string = tag.select("span.membership-type")[0].text
            match = re.search(r".*(\d{4})\).*", year_string)
            if match:
                person["year"] = match.group(1)

        if tag.select("span.primary_institution_text"):
            person["affiliation"] = tag.select("span.primary_institution_text em")[
                0
            ].text

        if tag.select("span.primary_section"):
            person["primary"] = tag.select(
                "span.primary_section .primary_section_text"
            )[0].text

        if tag.select("span.secondary_section"):
            person["secondary"] = tag.select(
                "span.secondary_section .secondary_section_text"
            )[0].text

    except Exception as e:
        print(name, e)
        break

    members.append(person)

dump(members, open("data/nas-members.json", "w", encoding="utf8"))
