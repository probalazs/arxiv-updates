from dataclasses import dataclass
from typing import TypedDict


@dataclass
class XMLFeed:
    updated: str


@dataclass
class XMLEntry:
    title: str
    summary: str
    link: str


@dataclass
class XML:
    feed: XMLFeed
    entries: list[XMLEntry]


class ReleaseFeed(TypedDict):
    updated: str


class ReleasePaper(TypedDict):
    title: str
    summary: str
    link: str


class ReleaseContent(TypedDict):
    feed: ReleaseFeed
    papers: list[ReleasePaper]


class Release(TypedDict):
    content: ReleaseContent
    filename: str
