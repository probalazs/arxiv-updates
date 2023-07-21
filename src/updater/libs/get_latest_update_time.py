import base64
from datetime import datetime
import json

from src.updater.libs.get_datetime_from_release_date import (
    get_datetime_from_release_date,
)
from ramda import pipe


def get_lates_update_time(release_filenames: list[str]) -> datetime:
    return pipe(
        _get_decoded_filenames,
        _get_updated_times,
        max,
    )(release_filenames)


def _get_updated_times(decoded_filenames: list[dict]) -> list[datetime]:
    return [
        get_datetime_from_release_date(filename["updated"])
        for filename in decoded_filenames
    ]


def _get_decoded_filenames(filenames: list[str]) -> list[dict]:
    return [_get_decoded_filename(filename) for filename in filenames]


def _get_decoded_filename(filename: str) -> dict:
    return json.loads(base64.b64decode(filename[:-5]).decode("utf-8"))
