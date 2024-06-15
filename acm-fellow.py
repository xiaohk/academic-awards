import requests
from bs4 import BeautifulSoup
from json import load, dump

url = "https://awards.acm.org/award_winners?year=&award=158&region=&submit=Submit&isSpecialCategory="
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")


fellows = []
trs = soup.find_all("tr")


for tr in trs:
    tds = tr.find_all("td")

    if len(tds) == 5:
        # Replace non-breaking space
        name = tds[0].text.replace("\xa0", " ")

        # Swap the first/last name order
        parts = name.split(", ")
        name_swapped = parts[1] + " " + parts[0]

        fellows.append({"name": name_swapped, "year": tds[2].text})

# Sort the fellows by the year
fellows.sort(key=lambda x: x["year"], reverse=True)

dump(fellows, open("./data/acm-fellows.json", "w", encoding="utf8"))
