import feedparser
from pytest_httpserver import HTTPServer
from src.updater.libs.get_paper_updates import get_paper_updates_xml
from tests.helpers import get_fixture_xml


def test__get_paper_updates__returns_paresed_content_from_url(
    httpserver: HTTPServer,
) -> None:
    response = get_fixture_xml()
    httpserver.expect_request("/test").respond_with_data(response)

    result = get_paper_updates_xml(httpserver.url_for("/test"))

    assert result == feedparser.parse(response)
