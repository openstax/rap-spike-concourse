import json
import sys

from src.event_api import get_events
from src.utils import msg


def check(in_stream):
    input = json.load(in_stream)
    api_root = input["source"]["api_root"]
    status = input["source"]["status"]

    events = get_events(api_root)
    msg("{}", events)

    events = [event for event in events if event["status"] == status]

    if input["version"]:
        previous_id = input["version"]["id"]
        events = [event for event in events if event["id"] > previous_id]

    return [{"id": event["id"]} for event in events]


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == "__main__":
    main()
