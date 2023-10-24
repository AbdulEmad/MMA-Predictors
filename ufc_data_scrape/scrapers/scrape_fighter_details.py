import re
import datetime

import requests
from bs4 import BeautifulSoup as bs


def get_fighter_urls(letter):
    urls = []
    current_url = f"http://ufcstats.com/statistics/fighters?char={letter}&page=all"
    response = requests.get(current_url)
    soup = bs(response.content, "html.parser")
    rows = soup.find(
        "table", attrs={"class", "b-statistics__table"}
    ).find('tbody').find_all('tr')

    for row in rows:
        try:
            urls.append(row.find_next("tr").find_next("a").get("href"))
        except:
            pass
    return urls


def get_fighter_info(url: str) -> dict:
    fighter_info = {}
    response = requests.get(url)
    soup = bs(response.content, "html.parser")

    # GETS FIGHTER DETAILS
    fighter_info["name"] = soup.find(attrs={"class", "b-content__title-highlight"}).text.strip()
    fighter_info = fighter_info | convert_fighter_features("Record", soup.find(
        attrs={"class", "b-content__title-record"}).text.strip().split(" ")[1])

    # TALE OF THE TAPE AND CAREER STATISTICS
    fighter_details = soup.findAll(
        "li", attrs={"class", "b-list__box-list-item b-list__box-list-item_type_block"}
    )

    for attribute in fighter_details:
        try:
            key, value = "".join(attribute.text.split()).split(":")
            fighter_info = fighter_info | convert_fighter_features(key, value)
        except:
            pass

    return fighter_info


def convert_fighter_features(feature, value):
    today = datetime.date.today()
    year = today.year

    def height(var):
        result = var.split("'")
        result = int(result[0]) * 12 + int(result[1].strip('"'))
        result *= 2.54
        return result

    def clean_str_to_float(var):
        return float(re.sub("\D", "", var))

    def stance(var):
        return var

    def age(var):
        return year - int(var.split(",")[1])

    def record(var):
        record = var.split("-")
        win = int(re.sub("\D", "", record[0]))
        return {"win": win, "loss": int(record[1]), "draw": int(record[2])}

    features = {
        "Height": height,
        "Weight": clean_str_to_float,
        "Reach": clean_str_to_float,
        "STANCE": stance,
        "DOB": age,
        "SLpM": float,
        "Str.Acc.": clean_str_to_float,
        "SApM": float,
        "Str.Def": clean_str_to_float,
        "TDAvg.": float,
        "TDAcc.": clean_str_to_float,
        "TDDef.": clean_str_to_float,
        "Sub.Avg.": float,
        "Record": record
    }

    keys_clean = {
        "Height": "height",
        "Weight": "weight",
        "Reach": "reach",
        "STANCE": "stance",
        "DOB": "age",
        "SLpM": "slpm",
        "Str.Acc.": "str_acc",
        "SApM": "sapm",
        "Str.Def": "str_def",
        "TDAvg.": "td_avg",
        "TDAcc.": "td_acc",
        "TDDef.": "td_def",
        "Sub.Avg.": "sub_avg",
        "Record": None
    }

    try:
        if keys_clean[feature] is None:
            return features[feature](value)
        else:
            return {keys_clean[feature]: features[feature](value)}
    except:
        return {keys_clean[feature]: None}

