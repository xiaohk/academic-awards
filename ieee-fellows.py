import requests
import urllib.parse
import time

from bs4 import BeautifulSoup
from json import load, dump
from tqdm import tqdm
from requests_ip_rotator import ApiGateway


def scrape_ieee_fellow_page(session, page_num):

    url = "https://services27.ieee.org/fellowsdirectory/getpageresultsdesk.html"

    data = {
        "selectedJSON": {
            "alpha": "ALL",
            "menu": "ALPHABETICAL",
            "gender": "All",
            "currPageNum": "1",
            "breadCrumbs": [{"breadCrumb": "Alphabetical Listing "}],
            "helpText": "Click on any of the alphabet letters to view a list of Fellows.",
        },
        "inputFilterJSON": {
            "sortOnList": [{"sortByField": "fellow.lastName", "sortType": "ASC"}],
            "typeAhead": "false",
        },
        "pageNum": f"{page_num}",
    }

    header = {
        "Host": "services27.ieee.org",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "457",
        "Origin": "https://services27.ieee.org",
        "Connection": "keep-alive",
        "Referer": "https://services27.ieee.org/fellowsdirectory/home.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
    }

    response = session.post(
        url, data=urllib.parse.urlencode(data), headers=header, timeout=120
    )

    soup = BeautifulSoup(response.text, "html.parser")

    # Parse the HTML output
    fellows = []

    trs = soup.select("div.tr")
    for tr in trs:
        name = tr.select("div.name")[0].find("span").text

        # Swap the first/last name order
        parts = name.split(", ")
        name_swapped = parts[1] + " " + parts[0]

        region = (
            tr.select("div.region")[0]
            .find("a")
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        year = int(
            tr.select("div.class")[0]
            .find("a")
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        citation = (
            tr.select("div.citation")[0]
            .text.replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
        )

        # Parse category (only keep the first one if any)
        category_tags = tr.select("div.category")
        category = ""

        for tag in category_tags:
            if tag.text != "":
                category = (
                    tag.text.replace("\t", "").replace("\n", "").replace("\r", "")
                )
                break

        fellows.append(
            {
                "name": name_swapped,
                "region": region,
                "year": year,
                "category": category,
                "citation": citation,
            }
        )

    return fellows


# Initial request to figure out the number of pages
url = "https://services27.ieee.org/fellowsdirectory/home.html"
header = {
    "Host": "services27.ieee.org",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
}

response = requests.get(url, headers=header, timeout=120)
soup = BeautifulSoup(response.text, "html.parser")

max_page_num = 0

li_tags = soup.select("li.digit")
for tag in li_tags:
    if tag.find("a"):
        page_num = int(tag.find("a").text)
        max_page_num = max(page_num, max_page_num)

all_fellows = []
error_pages = []

gateway = ApiGateway("https://services27.ieee.org")
gateway.start()

session = requests.Session()
session.mount("https://services27.ieee.org", gateway)

for p in tqdm(range(1, max_page_num + 1)):
    try:
        cur_fellows = scrape_ieee_fellow_page(session, p)
        all_fellows.extend(cur_fellows)

        if len(cur_fellows) == 0:
            error_pages.append(p)
            print("No author on page ", p)

    except:
        print("Error on page ", p)
        error_pages.append(p)
        continue

    if p % 500 == 0:
        dump(all_fellows, open("data/ieee-fellows.json", "w", encoding="utf8"))

dump(all_fellows, open("data/ieee-fellows.json", "w", encoding="utf8"))
gateway.shutdown()
