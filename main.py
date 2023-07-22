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
from src.configuration import rss, updates_releases_bucket
import functions_framework
import google.cloud.logging


@functions_framework.http
def main(_) -> None:
    _setup_logging()
    _run_updaload()


def _run_updaload() -> None:
    UploadNewRelease(
        client=storage_client(),
        get_paper_updates=get_paper_updates_xml,
        get_latest_update_time=get_lates_update_time,
        get_release=get_release,
        get_blob_names_from_storage=get_blob_names_from_storage,
        upload_release_to_storage=upload_release_to_storage,
        get_datetime_from_release_date=get_datetime_from_release_date,
    )(rss(), updates_releases_bucket())


def _setup_logging() -> None:
    client = google.cloud.logging.Client()
    client.setup_logging()
