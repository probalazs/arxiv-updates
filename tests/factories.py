from dataclasses import dataclass
from datetime import datetime

from src.interface import XML


@dataclass
class TestXMLFeed:
    updated: str


@dataclass
class TestXMLEntry:
    title: str
    summary: str
    link: str


@dataclass
class TestXML:
    feed: TestXMLFeed
    entries: list[TestXMLEntry]


def get_xml(override=None) -> TestXML:
    feed = override.get("feed", {"updated": datetime.now().isoformat()})
    entries = override.get("entries", [])
    return TestXML(
        feed=TestXMLFeed(**feed), entries=[TestXMLEntry(**entry) for entry in entries]
    )
