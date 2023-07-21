import uuid


def get_random_string() -> str:
    return str(uuid.uuid4())
