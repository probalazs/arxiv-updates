from typing import Any, TypedDict

XML = Any


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
