from datetime import datetime, timezone
from src.updater.libs.get_datetime_from_release_date import (
    get_datetime_from_release_date,
)


def test__get_datetime_from_release_date__returns_datetime_from_release_date() -> None:
    release_date = "2021-08-01T00:00:00+00:00"
    expected = datetime(2021, 8, 1, 0, 0, 0, tzinfo=timezone.utc).isoformat()

    result = get_datetime_from_release_date(release_date)

    assert result == expected
