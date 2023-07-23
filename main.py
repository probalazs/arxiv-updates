from typing import Any
from src.updater.upload_new_release import UploadNewRelease
from src.libs.clients import storage_client
from src.updater.libs.get_blob_names_from_storage import get_blob_names_from_storage
from src.updater.libs.get_datetime_from_release_date import (
    get_datetime_from_release_date,
)
from src.updater.libs.get_latest_update_time import get_lates_update_time
from src.updater.libs.get_paper_updates import get_paper_updates_xml
from src.updater.libs.upload_release_to_storage import upload_release_to_storage
from src.updater.libs.get_release import get_release
import functions_framework
import google.cloud.logging


@functions_framework.http
def main(request: Any) -> None:
    body = request.get_json(silent=True)
    _setup_logging()
    _run_updaload(body["rss"], body["bucket"])
    return "", 200


def _run_updaload(rss: str, bucket: str) -> None:
    UploadNewRelease(
        client=storage_client(),
        get_paper_updates=get_paper_updates_xml,
        get_latest_update_time=get_lates_update_time,
        get_release=get_release,
        get_blob_names_from_storage=get_blob_names_from_storage,
        upload_release_to_storage=upload_release_to_storage,
        get_datetime_from_release_date=get_datetime_from_release_date,
    )(rss, bucket)


def _setup_logging() -> None:
    client = google.cloud.logging.Client()
    client.setup_logging()
