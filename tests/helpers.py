import os
import uuid


def get_random_string() -> str:
    return str(uuid.uuid4())


def get_fixture_xml():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    fixture = os.path.join(current_directory, "fixtures", "updates.xml")
    with open(fixture, "r") as f:
        content = f.read()
    return content
