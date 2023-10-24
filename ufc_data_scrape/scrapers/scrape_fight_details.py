import requests
from bs4 import BeautifulSoup as bs


def get_fight_urls(event_url):
    response = requests.get(event_url)
    soup = bs(response.content, "html.parser")
    urls=[]

    rows = soup.find(
        "table", attrs={"class", "b-fight-details__table b-fight-details__table_style_margin-top "
                                 "b-fight-details__table_type_event-details js-fight-table"}
    ).find('tbody').find_all('tr')

    for row in rows:
        try:
            urls.append(row.find_next("a").get("href"))
        except:
            pass

    return urls


def get_fight_details(fight_url: str):
    response = requests.get(fight_url)
    soup = bs(response.content, "html.parser")
    fight_details = {}

    fight_details = fight_details | parse_person_details(soup.find_all(attrs={"class", "b-fight-details__person"}))
    fight_details = fight_details | parse_general_details(soup.find(attrs={"class", "b-fight-details__fight"}))

    details_tables = soup.find_all(attrs={"class", "b-fight-details__table-body"})

    fight_details = fight_details | parse_totals_details(details_tables[0].find_all(
        attrs={"class", "b-fight-details__table-col"}))

    fight_details = fight_details | parse_strike_details(
        details_tables[2].find_all(attrs={"class", "b-fight-details__table-col"}))

    return fight_details


def parse_person_details(persons):
    person_details = {}
    person_details["fighter_1"] = persons[0].find(attrs={"class", "b-fight-details__person-name"}).text.strip()
    person_details["fighter_2"] = persons[1].find(attrs={"class", "b-fight-details__person-name"}).text.strip()
    person_details["result_fighter_1"] = persons[0].find(attrs={"class", "b-fight-details__person-status"}).text.strip()
    person_details["result_fighter_2"] = persons[1].find(attrs={"class", "b-fight-details__person-status"}).text.strip()

    return person_details


def parse_general_details(general_fight_details):
    general_details = {}
    general_details["title"] = general_fight_details.find(attrs={"class", "b-fight-details__fight-title"}).text.strip()
    general_details["method"] = \
        general_fight_details.find_next(attrs={"class", "b-fight-details__text-item_first"}).text.split(":")[1].strip()

    details = general_fight_details.find_all(attrs={"class", "b-fight-details__text-item"})
    for item in details[0:4]:
        item = item.text.strip().split(":")
        if item[0] == "Time":
            general_details["time"] = f"{item[1].strip()}:{item[2].strip()}"
        else:
            general_details[item[0].lower()] = item[1].strip()

    return general_details


def split_col_clean(column):
    return [s.strip() for s in column.text.strip().split("\n\n")]


def landed_thrown_clean(text):
    return [int(s.strip()) for s in text.split("of")]


def parse_totals_details(totals_columns):
    totals_details = {}

    totals_details["kd_fighter_1"], totals_details["kd_fighter_2"] = split_col_clean(totals_columns[1])

    sig_thrown_landed = split_col_clean(totals_columns[2])
    totals_details["sig_landed_fighter_1"], totals_details["sig_thrown_fighter_1"] = landed_thrown_clean(
        sig_thrown_landed[0])
    totals_details["sig_landed_fighter_2"], totals_details["sig_thrown_fighter_2"] = landed_thrown_clean(
        sig_thrown_landed[1])

    td_thrown_landed = split_col_clean(totals_columns[5])
    totals_details["td_landed_fighter_1"], totals_details["td_thrown_fighter_1"] = landed_thrown_clean(
        td_thrown_landed[0])
    totals_details["td_landed_fighter_2"], totals_details["td_thrown_fighter_2"] = landed_thrown_clean(
        td_thrown_landed[1])

    totals_details["sub_att_fighter_1"], totals_details["sub_att_fighter_2"] = [int(s) for s in (split_col_clean(totals_columns[7]))]
    totals_details["rev_fighter_1"], totals_details["rev_fighter_2"] = [int(s) for s in (split_col_clean(totals_columns[8]))]
    totals_details["ctrl_fighter_1"], totals_details["ctrl_fighter_2"] = split_col_clean(totals_columns[9])

    return totals_details


def parse_strike_details(strike_columns):
    strike_details = {}

    head_thrown_landed = split_col_clean(strike_columns[3])
    strike_details["head_landed_fighter_1"], strike_details["head_thrown_fighter_1"] = landed_thrown_clean(
        head_thrown_landed[0])
    strike_details["head_landed_fighter_2"], strike_details["head_thrown_fighter_2"] = landed_thrown_clean(
        head_thrown_landed[1])

    body_thrown_landed = split_col_clean(strike_columns[4])
    strike_details["body_landed_fighter_1"], strike_details["body_thrown_fighter_1"] = landed_thrown_clean(
        body_thrown_landed[0])
    strike_details["body_landed_fighter_2"], strike_details["body_thrown_fighter_2"] = landed_thrown_clean(
        body_thrown_landed[1])

    leg_thrown_landed = split_col_clean(strike_columns[5])
    strike_details["leg_landed_fighter_1"], strike_details["leg_thrown_fighter_1"] = landed_thrown_clean(
        leg_thrown_landed[0])
    strike_details["leg_landed_fighter_2"], strike_details["leg_thrown_fighter_2"] = landed_thrown_clean(
        leg_thrown_landed[1])

    distance_thrown_landed = split_col_clean(strike_columns[6])
    strike_details["distance_landed_fighter_1"], strike_details["distance_thrown_fighter_1"] = landed_thrown_clean(
        distance_thrown_landed[0])
    strike_details["distance_landed_fighter_2"], strike_details["distance_thrown_fighter_2"] = landed_thrown_clean(
        distance_thrown_landed[1])

    clinch_thrown_landed = split_col_clean(strike_columns[7])
    strike_details["clinch_landed_fighter_1"], strike_details["clinch_thrown_fighter_1"] = landed_thrown_clean(
        clinch_thrown_landed[0])
    strike_details["clinch_landed_fighter_2"], strike_details["clinch_thrown_fighter_2"] = landed_thrown_clean(
        clinch_thrown_landed[1])

    ground_thrown_landed = split_col_clean(strike_columns[8])
    strike_details["ground_landed_fighter_1"], strike_details["ground_thrown_fighter_1"] = landed_thrown_clean(
        ground_thrown_landed[0])
    strike_details["ground_landed_fighter_2"], strike_details["ground_thrown_fighter_2"] = landed_thrown_clean(
        ground_thrown_landed[1])

    return strike_details