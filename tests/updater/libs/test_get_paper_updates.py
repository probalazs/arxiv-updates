import feedparser
import os
from pytest_httpserver import HTTPServer
from src.updater.libs.get_paper_updates import get_paper_updates_xml


def test__get_paper_updates__returns_paresed_content_from_url(
    httpserver: HTTPServer,
) -> None:
    response = get_fixture_xml()
    httpserver.expect_request("/test").respond_with_data(response)

    result = get_paper_updates_xml(httpserver.url_for("/test"))

    assert result == feedparser.parse(response)


def get_fixture_xml():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    fixture = os.path.join(current_directory, "fixtures", "updates.xml")
    with open(fixture, "r") as f:
        content = f.read()
    return content
