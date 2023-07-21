import base64
import json

from src.interface import XML, Release, ReleaseContent, ReleaseFeed, ReleasePaper


def get_release(xml: XML) -> Release:
    return {
        "content": _get_file_content(xml),
        "filename": _get_filename(xml),
    }


def _get_file_content(xml: XML) -> ReleaseContent:
    return {
        "feed": _get_feed(xml),
        "papers": _get_papers(xml),
    }


def _get_filename(xml: XML) -> str:
    return (
        base64.b64encode(
            json.dumps({"updated": xml.feed.updated}).encode("utf-8")
        ).decode("utf-8")
        + ".json"
    )


def _get_feed(xml: XML) -> ReleaseFeed:
    return {
        "updated": xml.feed.updated,
    }


def _get_papers(xml: XML) -> list[ReleasePaper]:
    return [_get_paper(entity) for entity in xml.entries]


def _get_paper(entity: dict) -> ReleasePaper:
    return {
        "title": entity.title,
        "summary": entity.summary,
        "link": entity.link,
    }
