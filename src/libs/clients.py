from functools import lru_cache
from google.cloud import storage
from src.configuration import application_service_account, project_id
from google.auth import impersonated_credentials, default, credentials

_CLOUD_PLATFORM_TARGET_SCOPES = "https://www.googleapis.com/auth/cloud-platform"


@lru_cache()
def _get_credentials() -> credentials.Credentials:
    credentials, _ = default()
    if not application_service_account():
        return credentials
    return impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=application_service_account(),
        target_scopes=_CLOUD_PLATFORM_TARGET_SCOPES,
    )


@lru_cache()
def storage_client() -> storage.Client:
    return storage.Client(
        project=project_id(),
        credentials=_get_credentials(),
    )
