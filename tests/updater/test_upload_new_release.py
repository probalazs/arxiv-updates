from datetime import datetime, timedelta
from unittest.mock import Mock
from tests.factories import get_release, get_xml
from tests.helpers import get_random_string
from src.updater.upload_new_release import UploadNewRelease
from google.cloud.storage import Client


def test__upload_new_release__fetch_paper_udpates_from_rss() -> None:
    rss = get_random_string
    get_paper_updates = Mock()

    create_update_new_release(
        {
            "get_paper_updates": get_paper_updates,
        }
    )(rss, get_random_string())

    get_paper_updates.assert_called_once_with(rss)


def test__upload_new_release__get_release_from_paper_updates() -> None:
    xml = get_xml()
    get_paper_updates = Mock(return_value=xml)
    get_release = Mock()
    create_update_new_release(
        {
            "get_paper_updates": get_paper_updates,
            "get_release": get_release,
        }
    )(get_random_string(), get_random_string())

    get_release.assert_called_once_with(xml)


def test__upload_new_release__get_blob_names_from_storage() -> None:
    bucket = get_random_string()
    get_blob_names_from_storage = Mock()
    client = Mock(spec=Client)
    create_update_new_release(
        {
            "client": client,
            "get_blob_names_from_storage": get_blob_names_from_storage,
        }
    )(get_random_string(), bucket)

    get_blob_names_from_storage.assert_called_once_with(client, bucket)


def test__upload_new_release__has_uploaded_blobs_and_has_no_update__get_latest_udpate_time_from_blob_names() -> (
    None
):
    latest_update_time = datetime.now()
    blob_names = [get_random_string()]
    get_latest_update_time = Mock(return_value=latest_update_time)
    get_blob_names_from_storage = Mock(return_value=blob_names)
    create_update_new_release(
        {
            "get_latest_update_time": get_latest_update_time,
            "get_blob_names_from_storage": get_blob_names_from_storage,
        }
    )(get_random_string(), get_random_string())

    get_latest_update_time.assert_called_once_with(blob_names)


def test__upload_new_releases__has_uploaded_blobs_and_has_no_update__convert_datetime_from_release_date() -> (
    None
):
    release = get_release()
    latest_update_time = datetime.now()
    get_release_mock = Mock(return_value=release)
    get_latest_update_time = Mock(return_value=latest_update_time)
    get_blob_names_from_storage = Mock(return_value=[get_random_string()])
    get_datetime_from_release_date = Mock(return_value=datetime.now())
    create_update_new_release(
        {
            "get_latest_update_time": get_latest_update_time,
            "get_blob_names_from_storage": get_blob_names_from_storage,
            "get_datetime_from_release_date": get_datetime_from_release_date,
            "get_release": get_release_mock,
        }
    )(get_random_string(), get_random_string())

    get_datetime_from_release_date.assert_called_once_with(
        release["content"]["feed"]["updated"]
    )


def test__upload_new_release__has_uploaded_blobs_and_has_update__upload_release_to_storage() -> (
    None
):
    latest_update_time = datetime.now() - timedelta(days=1)
    current_update_time = datetime.now()
    release = get_release()
    bucket = get_random_string()
    blob_names = [get_random_string()]
    get_release_mock = Mock(return_value=release)
    client = Mock(spec=Client)
    upload_release_to_storage = Mock()
    get_blob_names_from_storage = Mock(return_value=blob_names)
    get_latest_update_time = Mock(return_value=latest_update_time)
    get_datetime_from_release_date = Mock(return_value=current_update_time)
    create_update_new_release(
        {
            "client": client,
            "upload_release_to_storage": upload_release_to_storage,
            "get_latest_update_time": get_latest_update_time,
            "get_blob_names_from_storage": get_blob_names_from_storage,
            "get_release": get_release_mock,
            "get_datetime_from_release_date": get_datetime_from_release_date,
        }
    )(get_random_string(), bucket)

    upload_release_to_storage.assert_called_once_with(client, bucket, release)


def test__upload_new_release__has_no_uploaded_blobs__upload_release_to_storage() -> (
    None
):
    blob_names = []
    release = get_release()
    bucket = get_random_string()
    get_release_mock = Mock(return_value=release)
    client = Mock(spec=Client)
    upload_release_to_storage = Mock()
    get_blob_names_from_storage = Mock(return_value=blob_names)
    create_update_new_release(
        {
            "client": client,
            "upload_release_to_storage": upload_release_to_storage,
            "get_blob_names_from_storage": get_blob_names_from_storage,
            "get_release": get_release_mock,
        }
    )(get_random_string(), bucket)

    upload_release_to_storage.assert_called_once_with(client, bucket, release)


def test__upload_new_release__has_uploaded_blobs_and_has_no_update__does_not_upload_release_to_storage() -> (
    None
):
    update_time = datetime.now()
    blob_names = [get_random_string()]
    get_latest_update_time = Mock(return_value=update_time)
    get_blob_names_from_storage = Mock(return_value=blob_names)
    upload_release_to_storage = Mock()
    get_datetime_from_release_date = Mock(return_value=update_time)
    create_update_new_release(
        {
            "get_latest_update_time": get_latest_update_time,
            "get_blob_names_from_storage": get_blob_names_from_storage,
            "upload_release_to_storage": upload_release_to_storage,
            "get_datetime_from_release_date": get_datetime_from_release_date,
        }
    )(get_random_string(), get_random_string())

    upload_release_to_storage.assert_not_called()


def create_update_new_release(override=None) -> UploadNewRelease:
    return UploadNewRelease(
        **{
            "client": Mock(spec=Client),
            "get_paper_updates": Mock(return_value=get_xml()),
            "get_latest_update_time": Mock(return_value=datetime.now()),
            "get_release": Mock(return_value=get_release()),
            "get_blob_names_from_storage": Mock(return_value=[]),
            "upload_release_to_storage": Mock(),
            "get_datetime_from_release_date": Mock(return_value=datetime.now()),
            **(override or {}),
        }
    )
