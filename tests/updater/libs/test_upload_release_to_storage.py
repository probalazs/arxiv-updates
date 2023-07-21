import json
from unittest.mock import Mock
from tests.factories import get_release
from tests.helpers import get_random_string
from src.updater.libs.upload_release_to_storage import upload_release_to_storage
from google.cloud.storage import Client, Bucket, Blob


def test__upload_release_to_storage__fetch_the_given_bucket() -> None:
    bucket_name = get_random_string()
    blob = Mock(spec=Blob)
    bucket = Mock(spec=Bucket)
    bucket.blob.return_value = blob
    storage_client = Mock(spec=Client)
    storage_client.bucket.return_value = bucket

    upload_release_to_storage(storage_client, bucket_name, get_release())

    storage_client.bucket.assert_called_once_with(bucket_name)


def test__upload_release_to_storage__fetch_the_given_blob() -> None:
    release = get_release()
    blob = Mock(spec=Blob)
    bucket = Mock(spec=Bucket)
    bucket.blob.return_value = blob
    storage_client = Mock(spec=Client)
    storage_client.bucket.return_value = bucket

    upload_release_to_storage(storage_client, get_random_string(), release)

    bucket.blob.assert_called_once_with(release["filename"])


def test__upload_release_to_storage__upload_the_release() -> None:
    release = get_release()
    blob = Mock(spec=Blob)
    bucket = Mock(spec=Bucket)
    bucket.blob.return_value = blob
    storage_client = Mock(spec=Client)
    storage_client.bucket.return_value = bucket

    upload_release_to_storage(storage_client, get_random_string(), release)

    blob.upload_from_string.assert_called_once_with(
        data=json.dumps(release["content"]),
        content_type="application/json",
    )
