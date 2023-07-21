import feedparser
import requests


def get_paper_updates_xml(url: str) -> dict:
    response = requests.get(url)
    return feedparser.parse(response.content)
