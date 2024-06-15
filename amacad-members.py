import requests
import urllib.parse
import time

from bs4 import BeautifulSoup
from json import load, dump
from tqdm import tqdm


def scrape_amacad_members(page_num):
    url_data = {
        "field_class_section": "All",
        "field_class_section_1": "All",
        "field_deceased": "All",
        "sort_bef_combine": "field_election_year_DESC",
        "_wrapper_format": "drupal_ajax",
        "view_name": "members",
        "view_display_id": "members",
        "view_args": "",
        "view_path": "/directory",
        "view_base_path": "directory",
        "view_dom_id": "8a3fd590c3840c5bbb77185f26f190b31b76d7659d947fdbfcd56098fd3e302e",
        "pager_element": "0",
        "field_affiliation": "",
        "field_class_section": "All",
        "field_class_section_1": "All",
        "field_deceased": "All",
        "sort_bef_combine": "field_election_year_DESC",
        "search_api_fulltext": "",
        "field_election_year": "",
        "page": f"{page_num}",
        "_drupal_ajax": "1",
        "ajax_page_state[theme]": "amacad",
        "ajax_page_state[theme_token]": "",
        "ajax_page_state[libraries]": "eJx1UNGOwzAI-6Go-aQIFppmIqECsq339ZdN1aaddC_YWJaRgSs8Egtk0ggfvvimgkgaoMEFciwsCByQ3EkTPXYxymmtPFeLMFySDWzV_7MU6qQzIYMDwzHPIW1wq6IWVhHv4mTxzUIRKUwJOvDh9TID_ghhh0I6c9pgrzt0CnaYU4sIRuFW6W7xNZdnsS-hSR58etKr9lbNRY94YrgTrqItnrjkCiwl_AzFtMros0aVfr7lF-uLgLw",
    }

    base_url = "https://www.amacad.org/views/ajax?"
    query_url = base_url + urllib.parse.urlencode(url_data)

    header = {
        "Host": "www.amacad.org",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "https://www.amacad.org/directory?field_class_section=All&field_class_section_1=All&field_deceased=All&sort_bef_combine=field_election_year_DESC&page=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=1",
    }

    response = requests.get(query_url, headers=header)

    commands = response.json()

    people = []

    for command in commands:
        if command["command"] == "insert" and command["data"] != "":
            data = command["data"]
            soup = BeautifulSoup(data, "html.parser")

            cards = soup.select("article.person-card")

            for card in cards:
                name = (
                    card.select("span.person__full-name")[0]
                    .text.replace("\t", "")
                    .replace("\n", "")
                    .replace("\r", "")
                )

                person = {
                    "name": name,
                    "affiliation": "",
                    "area": "",
                    "specialty": "",
                    "year": "",
                }

                if card.select("div.person__affiliation div.field-item"):
                    person["affiliation"] = (
                        card.select("div.person__affiliation div.field-item")[0]
                        .text.replace("\t", "")
                        .replace("\n", "")
                        .replace("\r", "")
                    )

                # The inline fields
                fields = card.select("div.person-card-directory__field")

                for field in fields:
                    label = (
                        field.select("div.person-card-directory__label")[0]
                        .text.replace("\t", "")
                        .replace("\n", "")
                        .replace("\r", "")
                    )
                    value = (
                        field.select("div.person-card-directory__value")[0]
                        .text.replace("\t", "")
                        .replace("\n", "")
                        .replace("\r", "")
                    )

                    if label == "Area:":
                        person["area"] = value
                    elif label == "Specialty:":
                        person["specialty"] = value
                    elif label == "Elected:":
                        person["year"] = value

                people.append(person)

    return people


# Initial request to figure out the number of pages
url = "https://www.amacad.org/directory"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
}

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

max_page_num = int(
    soup.select(".pager li.pager__item span[aria-hidden][role]")[0].text.split(" of ")[
        1
    ]
)

all_fellows = []
error_pages = []

session = requests.Session()

for p in tqdm(range(0, max_page_num)):
    try:
        cur_fellows = scrape_amacad_members(p)
        all_fellows.extend(cur_fellows)

        if len(cur_fellows) == 0:
            error_pages.append(p)
            print("No author on page ", p)

    except:
        print("Error on page ", p)
        error_pages.append(p)
        continue

    if p % 100 == 0:
        dump(all_fellows, open("../data/amacad-members.json", "w", encoding="utf8"))

dump(all_fellows, open("../data/amacad-members.json", "w", encoding="utf8"))
