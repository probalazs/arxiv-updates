from tests.factories import get_xml
from src.updater.libs.get_release import get_release
from tests.helpers import get_random_string


def test__get_release__returns_with_filename() -> None:
    update = "2021-07-21T20:20:20Z"
    xml = get_xml({"feed": {"updated": update}})

    release = get_release(xml)

    assert (
        release["filename"] == "eyJ1cGRhdGVkIjogIjIwMjEtMDctMjFUMjA6MjA6MjBaIn0=.json"
    )


def test__get_release__returns_with_feed() -> None:
    update = "2021-07-21T20:20:20Z"
    xml = get_xml({"feed": {"updated": update}})

    release = get_release(xml)

    assert release["content"]["feed"] == {"updated": update}


def test__get_release__returns_with_papers() -> None:
    title = get_random_string()
    summary = get_random_string()
    link = get_random_string()
    xml = get_xml(
        {
            "entries": [
                {
                    "title": title,
                    "summary": summary,
                    "link": link,
                }
            ]
        }
    )

    release = get_release(xml)

    assert release["content"]["papers"] == [
        {
            "title": title,
            "summary": summary,
            "link": link,
        }
    ]
