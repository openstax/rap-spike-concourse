from datetime import datetime
from flask import Flask, jsonify, request, render_template, abort

EVENTS = []


def create_app():
    settings = {
        'DEBUG': True,
    }
    app = Flask(__name__)
    app.config.update(settings)
    return app


app = create_app()


def _get_events():
    return EVENTS


def _get_event(id):
    for event in EVENTS:
        if event["id"] == str(id):
            return event

    return None


def _save_event(event):
    EVENTS.append(event)


@app.route('/events', methods=['GET'])
def list_events():
    events = _get_events()
    return jsonify(dict(events=events))


@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = _get_event(id)
    if event:
        return jsonify(event)
    else:
        return abort(404)


@app.route('/events', methods=['POST'])
def add_event():
    event = request.get_json()
    if not event: abort(400, "No event to add")

    ident_hash = event.get('ident_hash')
    if not ident_hash: abort(400, "Missing 'ident_hash'")

    event_id = str(len(_get_events()) + 1)
    event.update(dict(
        id=event_id,
        created_at=datetime.utcnow().isoformat(),
    ))

    _save_event(event)

    return jsonify(
        dict(status=201, response=event, mimetype="application/json")
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
