import requests
from bs4 import BeautifulSoup
from json import load, dump


def scrape_acm_awards(award_id, file_name):
    """
    Scrapes the ACM awards website for information about ACM awards.

    Args:
        award_id (str): The ID of the award to scrape.
        file_name (str): The name of the file to save the scraped data.
    """

    url = f"https://awards.acm.org/award_winners?year=&award={award_id}&region=&submit=Submit&isSpecialCategory="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
    }

    response = requests.get(url, headers=headers, timeout=120)

    soup = BeautifulSoup(response.text, "html.parser")

    trs = soup.find_all("tr")

    fellows = []

    for tr in trs:
        tds = tr.find_all("td")

        if len(tds) == 5:
            # Replace non-breaking space
            name = tds[0].text.replace("\xa0", " ")

            # Swap the first/last name order
            parts = name.split(", ")
            name_swapped = parts[1] + " " + parts[0]

            fellows.append({"name": name_swapped, "year": tds[2].text})

    # Sort the fellows by year and first name
    fellows.sort(key=lambda x: x["name"], reverse=False)
    fellows.sort(key=lambda x: x["year"], reverse=True)

    dump(fellows, open(file_name, "w", encoding="utf8"))


scrape_acm_awards(158, "data/acm-fellow.json")
scrape_acm_awards(157, "data/acm-distinguished-member.json")
scrape_acm_awards(159, "data/acm-senior-member.json")
scrape_acm_awards(140, "data/acm-turing-award.json")
scrape_acm_awards(146, "data/acm-dissertation-award.json")
scrape_acm_awards(160, "data/acm-gordon-bell-prize.json")
scrape_acm_awards(145, "data/acm-grace-murray-hopper-award.json")
