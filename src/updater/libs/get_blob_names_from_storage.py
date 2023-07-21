from google.cloud.storage import Client


def get_blob_names_from_storage(client: Client, bucket_name: str) -> list[str]:
    blobs = client.list_blobs(bucket_name)
    return [blob.name for blob in blobs]
