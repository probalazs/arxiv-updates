import os
import signal
from subprocess import Popen
from time import sleep
import pytest
from gcp_storage_emulator.server import create_server
from pytest_httpserver import HTTPServer
import requests
from tests.helpers import get_fixture_xml, get_random_string
from unittest.mock import patch
from src.libs.clients import storage_client

WORKER_WAIT_TIME = 2
STORAGE_PORT = 9000
STORAGE_HOST = "localhost"
CLOUD_FUNCTION_PORT = 8090


def test__main__uploads_the_release(storage, cloud_function, httpserver: HTTPServer):
    xml = get_fixture_xml()
    httpserver.expect_request("/").respond_with_data(xml)
    worker_data = cloud_function(storage["emaulator_host"])

    requests.post(
        worker_data["cloud_function_url"],
        json={"rss": httpserver.url_for("/"), "bucket": storage["bucket"]},
    )

    with patch.dict(os.environ, {"STORAGE_EMULATOR_HOST": storage["emaulator_host"]}):
        assert get_blob_names(storage["bucket"]) == [
            "eyJ1cGRhdGVkIjogIjIwMjMtMDctMjBUMjA6MzA6MDAtMDU6MDAifQ==.json"
        ]


def get_blob_names(bucket: str):
    return [blob.name for blob in storage_client().get_bucket(bucket).list_blobs()]


@pytest.fixture
def storage():
    bucket = get_random_string()
    server = create_server(
        STORAGE_HOST, STORAGE_PORT, in_memory=True, default_bucket=bucket
    )
    server.start()
    yield {
        "emaulator_host": f"http://{STORAGE_HOST}:{STORAGE_PORT}",
        "bucket": bucket,
    }
    server.stop()


@pytest.fixture
def cloud_function():
    worker_process = {}

    def run(storage_emulator_host: str):
        worker_process["process"] = start_worker(
            {
                "STORAGE_EMULATOR_HOST": storage_emulator_host,
            },
            CLOUD_FUNCTION_PORT,
        )
        sleep(WORKER_WAIT_TIME)
        return {
            "cloud_function_url": f"http://localhost:{CLOUD_FUNCTION_PORT}",
        }

    yield run
    stop_worker(worker_process["process"])


def start_worker(environments: dict[str, str], port: int) -> Popen:
    return Popen(
        ["functions-framework", "--target", "main", "--port", str(port), "--debug"],
        env={**os.environ.copy(), **environments},
    )


def stop_worker(process: Popen) -> None:
    process.send_signal(signal.SIGTERM)
