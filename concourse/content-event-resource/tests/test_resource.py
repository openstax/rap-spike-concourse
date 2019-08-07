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


def make_input_stream(version):
    def make_stream(json_obj):
        stream = io.StringIO()
        json.dump(json_obj, stream)
        stream.seek(0)
        return stream

    def make_input(version):
        return {
            "source": {
                "api_root": "http://localhost:5000",
                "status": "queued"
            },
            "version": version,

        }

    return make_stream(make_input(version))


class TestCheck(object):

    @mock.patch("src.check.get_content_events")
    def test_edge_case(self, mock_fn):
        mock_fn.return_value = mock_content_event_api_response()

        version = None

        in_stream = make_input_stream(version)
        result = check.check(in_stream)

        assert result == [
            {"id": 1, "ident_hash": "0889907c-f0ef-496a-bcb8-2a5bb121717f", "status": "queued"},
            {"id": 2, "ident_hash": "02776133-d49d-49cb-bfaa-67c7f61b25a1", "status": "queued"}]
