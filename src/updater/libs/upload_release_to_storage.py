from google.cloud.storage import Client
import json

from src.interface import Release


def upload_release_to_storage(
    client: Client, bucket_name: str, release: Release
) -> None:
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(release["filename"])
    blob.upload_from_string(
        data=json.dumps(release["content"]),
        content_type="application/json",
    )
