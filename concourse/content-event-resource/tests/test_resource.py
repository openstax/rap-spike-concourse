import io
import json
import os
from unittest import mock

from src import check

DATA_DIR = os.path.join(os.path.realpath(os.path.dirname(__file__)), "data")


def read_json_file(filepath):
    with open(filepath) as infile:
        return json.load(infile)


def mock_content_event_api_response():
    return read_json_file(os.path.join(DATA_DIR, "content_events.json"))


def make_stream(json_obj):
    stream = io.StringIO()
    json.dump(json_obj, stream)
    stream.seek(0)
    return stream


def make_input(version, **kwargs):
    payload = {"source": {
        "api_root": "http://localhost:5000",
    },
        "version": version,
    }
    payload["source"].update(kwargs)

    return payload


def make_input_stream(version, **kwargs):
    return make_stream(make_input(version, **kwargs))


class TestCheck(object):

    @mock.patch("src.check.get_events")
    def test_edge_case_queued_events(self, mock_fn):
        mock_fn.return_value = mock_content_event_api_response()

        version = None

        in_stream = make_input_stream(version, status="queued")
        result = check.check(in_stream)

        assert result == [
            {"id": 1},
            {"id": 2}]

    @mock.patch("src.check.get_events")
    def test_edge_case_queued_no_events(self, mock_fn):
        mock_fn.return_value = []

        version = None

        in_stream = make_input_stream(version, status="queued")
        result = check.check(in_stream)

        assert result == []
