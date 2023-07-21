from dataclasses import dataclass
from unittest.mock import Mock
from tests.factories import get_blob
from tests.helpers import get_random_string
from google.cloud.storage import Client

from src.updater.libs.get_blob_names_from_storage import get_blob_names_from_storage


def test__get_blob_names_from_storage__returns_name_of_the_blobs_in_the_bucket() -> (
    None
):
    first_blob = get_blob()
    second_blob = get_blob()
    bucket = get_random_string()
    client = Mock(spec=Client)
    client.list_blobs.return_value = [first_blob, second_blob]

    blob_names = get_blob_names_from_storage(client, bucket)

    assert blob_names == [first_blob.name, second_blob.name]
