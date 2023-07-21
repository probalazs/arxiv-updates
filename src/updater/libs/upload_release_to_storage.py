from google.cloud.storage import Client
import json

from src.interface import Release


def upload_release_to_storage(client: Client, bucket: str, release: Release) -> None:
    bucket = client.bucket(bucket)
    blob = bucket.blob(release["filename"])
    blob.upload_from_string(
        data=json.dumps(release["content"]),
        content_type="application/json",
    )
