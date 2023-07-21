from datetime import datetime


def get_datetime_from_release_date(release_date: str) -> datetime:
    return datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%S%z").isoformat()
