from os import environ


def project_id() -> str:
    return environ.get("PROJECT_ID")


def application_service_account() -> str:
    return environ.get("APPLICATION_SERVICE_ACCOUNT")


def rss() -> str:
    return environ.get("RSS")


def updates_releases_bucket() -> str:
    return environ.get("UPDATES_RELEASE_BUCKET")
