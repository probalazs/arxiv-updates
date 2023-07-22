from dataclasses import dataclass
from datetime import datetime

from src.interface import XML, Release, ReleaseContent, ReleasePaper, XMLEntry, XMLFeed
from tests.helpers import get_random_string


def get_xml(override=None) -> XML:
    feed = (override or {}).get("feed", {"updated": datetime.now().isoformat()})
    entries = (override or {}).get("entries", [])
    return XML(feed=XMLFeed(**feed), entries=[XMLEntry(**entry) for entry in entries])


@dataclass
class TestBlob:
    name: str


def get_blob(override=None) -> TestBlob:
    return TestBlob(**{"name": get_random_string(), **(override or {})})


def get_release(override=None) -> Release:
    return {
        "filename": get_random_string(),
        "content": get_release_content(),
        **(override or {}),
    }


def get_release_content(override=None) -> ReleaseContent:
    return {
        "feed": get_release_feed(),
        "papers": [],
        **(override or {}),
    }


def get_release_feed(override=None) -> dict:
    return {
        "updated": datetime.now().isoformat(),
        **(override or {}),
    }


def get_release_paper(override=None) -> ReleasePaper:
    return {
        "title": get_random_string(),
        "summary": get_random_string(),
        "link": get_random_string(),
        **(override or {}),
    }
