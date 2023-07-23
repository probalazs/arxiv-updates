from os import environ


def application_service_account() -> str | None:
    return environ.get("APPLICATION_SERVICE_ACCOUNT")
