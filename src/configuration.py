from os import environ


def project_id() -> str:
    return environ["GCP_PROJECT"]


def application_service_account() -> str | None:
    return environ.get("APPLICATION_SERVICE_ACCOUNT")
