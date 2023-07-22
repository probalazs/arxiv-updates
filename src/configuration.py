from os import environ


def project_id() -> str:
    return environ["PROJECT_ID"]


def application_service_account() -> str:
    return environ["APPLICATION_SERVICE_ACCOUNT"]


def rss() -> str:
    return environ["RSS"]


def updates_releases_bucket() -> str:
    return environ["UPDATES_RELEASE_BUCKET"]
