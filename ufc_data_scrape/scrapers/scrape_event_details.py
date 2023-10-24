import requests
from bs4 import BeautifulSoup as bs


def get_event_urls() -> list:
    url = "http://ufcstats.com/statistics/events/completed?page=all"

    response = requests.get(url)
    soup = bs(response.content, "html.parser")

    rows = soup.find(
        "table", attrs={"class", "b-statistics__table-events"}
    ).find('tbody').find_all('tr')

    urls = []

    for row in rows:
        try:
            urls.append(row.find_next("tr").find_next("a").get("href"))
        except:
            pass

    return urls[1:]


def get_event_details(event_url: str) -> dict[str, ...]:
    response = requests.get(event_url)
    soup = bs(response.content, "html.parser")

    event_details = {"title": soup.find(attrs={"class", "b-content__title-highlight"}).text.strip()}

    header_details = soup.find_all(
        "li", attrs={"class", "b-list__box-list-item"}
    )
    event_details["date"] = header_details[0].text.split(":")[1].strip()
    event_details["location"] = header_details[1].text.split(":")[1].strip()

    return event_details


