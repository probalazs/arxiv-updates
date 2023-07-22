from os import environ


def project_id() -> str:
    return environ["GCP_PROJECT"]


def application_service_account() -> str | None:
    return environ.get("APPLICATION_SERVICE_ACCOUNT")


def rss() -> str:
    return environ["RSS"]


def updates_releases_bucket() -> str:
    return environ["UPDATES_RELEASE_BUCKET"]
