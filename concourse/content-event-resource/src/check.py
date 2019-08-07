import json
import sys

from src.events import get_content_events


def check(in_stream):
    input = json.load(in_stream)
    api_root = input["source"]["api_root"]
    status = input["source"]["status"]

    events = get_content_events(api_root)

    events = [event for event in events if event["status"] == status]

    if input["version"]:
        previous_id = input["version"]["id"]
        events = [event for event in events if event["id"] > previous_id]

    return events


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == "__main__":
    main()
