import base64
from datetime import datetime, timezone
import json

from src.updater.libs.get_latest_update_time import get_lates_update_time


def test__get_latest_update_time__received_one_release_filename__returns_the_only_udpate_time() -> (
    None
):
    updated = "2021-08-01T00:00:00+00:00"
    release_filenames = [
        get_filename({"updated": updated}),
    ]
    expected = datetime(2021, 8, 1, 0, 0, 0, tzinfo=timezone.utc).isoformat()

    result = get_lates_update_time(release_filenames)

    assert result == expected


def test__get_latest_update_time__received_two_release_filenames__returns_the_latest_update_time() -> (
    None
):
    updated_older = "2021-08-01T00:00:00+00:00"
    updated_newer = "2021-08-02T00:00:00+00:00"
    release_filenames = [
        get_filename({"updated": updated_older}),
        get_filename({"updated": updated_newer}),
    ]
    expected_newer = datetime(2021, 8, 2, 0, 0, 0, tzinfo=timezone.utc).isoformat()

    result = get_lates_update_time(release_filenames)

    assert result == expected_newer


def get_filename(data: dict) -> str:
    return encode_filename(json.dumps(data))


def encode_filename(filename: str) -> str:
    return base64.b64encode(filename.encode("utf-8")).decode("utf-8") + ".json"
