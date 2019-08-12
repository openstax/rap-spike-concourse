import requests


def build_url(api_root, *args):
    parts = [api_root]
    parts.extend(args)
    parts = [str(p) for p in parts]
    return "/".join(parts)


def get_events(api_root):
    url = build_url(api_root, "events")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["events"]


def get_event(api_root, event_id):
    url = build_url(api_root, "events", event_id)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
