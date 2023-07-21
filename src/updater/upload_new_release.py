from typing import Any, Callable
from google.cloud.storage import Client


class UploadNewRelease:
    def __init__(
        self,
        client: Client,
        get_paper_updates: Callable,
        get_latest_update_time: Callable,
        get_release: Callable,
        get_blob_names_from_storage: Callable,
        upload_release_to_storage: Callable,
        get_datetime_from_release_date: Callable,
    ):
        self._client = client
        self._get_paper_updates = get_paper_updates
        self._get_latest_update_time = get_latest_update_time
        self._get_release = get_release
        self._get_blob_names_from_storage = get_blob_names_from_storage
        self._upload_release_to_storage = upload_release_to_storage
        self._get_datetime_from_release_date = get_datetime_from_release_date

    def __call__(self, rss: str, bucket: str) -> None:
        xml = self._get_paper_updates(rss)
        file = self._get_release(xml)
        blob_names = self._get_blob_names_from_storage(self._client, bucket)

        if self._should_upload(blob_names, file):
            self._upload_release_to_storage(self._client, bucket, file)

    def _should_upload(self, blob_names: list[str], file: dict) -> bool:
        return not blob_names or self._is_new_release(blob_names, file)

    def _is_new_release(self, blob_names: list[str], file: dict) -> bool:
        latest_release = self._get_latest_update_time(blob_names)
        return latest_release < self._get_datetime_from_release_date(
            file["content"]["feed"]["updated"]
        )
