import pandas as pd
import scrapers.scrape_fighter_details as fighter_scraper
import scrapers.scrape_event_details as events_scraper
import scrapers.scrape_fight_details as fight_scraper
from string import ascii_lowercase as alc


def scrape_fighters():
    fighters = []
    for letter in alc:
        for url in fighter_scraper.get_fighter_urls(letter):
            fighters.append(fighter_scraper.get_fighter_info(url))

    fighters_df = pd.DataFrame(fighters)
    fighters_df.to_csv("fighters.csv")


def scrape_events_fights():
    fights = []
    events = []
    for url in events_scraper.get_event_urls():
        event = events_scraper.get_event_details(url)

        for fight in fight_scraper.get_fight_urls(url):
            fights.append({"event": event["title"]} | fight_scraper.get_fight_details(fight))

        events.append(event)

    fights_df = pd.DataFrame(fights)
    fights_df.to_csv("fights.csv")

    events_df = pd.DataFrame(events)
    events_df.to_csv(events)
