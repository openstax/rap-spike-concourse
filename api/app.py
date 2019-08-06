from datetime import datetime
from flask import Flask, jsonify, request, render_template, abort

events = []

def create_app():
    settings = {
        'DEBUG': True,
    }
    app = Flask(__name__)
    app.config.update(settings)
    return app

app = create_app()

def _get_events():
    return events

def _save_event(event):
    events.append(event)

@app.route('/events', methods=['GET'])
def list_events():
    events = _get_events()
    return jsonify(dict(events=events))

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    events = _get_events()
    try:
        event = next(event for event in events if event['id'] == id)
        return jsonify(dict(event=event))
    except:
        abort(404)

@app.route('/events', methods=['POST'])
def add_event():
    event = request.get_json()
    if not event: abort(400, "No event to add")

    ident_hash = event.get('ident_hash')
    if not ident_hash: abort(400, "Missing 'ident_hash'")

    event_id = len(_get_events()) + 1
    event.update(dict(
        id = event_id,
        created_at = datetime.utcnow().isoformat(),
    ))

    _save_event(event)

    return jsonify(
        dict(status=201, response=event, mimetype="application/json")
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
