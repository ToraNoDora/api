from flask import Flask, jsonify, abort, make_response, request


app = Flask(__name__)

notes = [
    {
        "id": 1,
        "title": "large multiline text",
        "text": "large multiline text", 
        "tags": ["tag1", "tag2", "tag3"]
    },
    {
        "id": 2,
        "title": "large multiline text",
        "text": "large multiline text", 
        "tags": ["tag1", "tag2", "tag3"]
    },
    {
        "id": 3,
        "title": "large multiline textooopppo",
        "text": "large multiline text", 
        "tags": ["tag1", "tag2", "tag3"]
    }
]


def search_note_request(note_id):
    note_request = [] 
    for note_id_new in notes:
        if note_id_new["id"] == note_id:
            return note_id_new
    abort(404)
    

# Все записи +
@app.route("/notes/api/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)


# Отдельная запись +
@app.route("/notes/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    return jsonify(search_note_request(note_id))


# Удаление записи +
@app.route("/notes/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes.remove(search_note_request(note_id))
    return jsonify({"result": True})


# Создание записи +
@app.route("/notes/api/notes", methods=["POST"])
def create_note():
    if not request.json or not "title" in request.json:
        abort(400)
    note_post = {
        "id": notes[-1]["id"] + 1,
        "title": request.json["title"],
        "text": request.json.get("text", ""),
        "tags": request.json.get("tags", "")
    }
    notes.append(note_post)
    return jsonify(note_post), 201


# Изменение записи +
@app.route("/notes/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    if not request.json:
        abort(400)
    note_put = search_note_request(note_id)
    note_put["title"] = request.json.get("title", note_put["title"])
    note_put["text"] = request.json.get("text", note_put["text"])
    note_put["tags"] = request.json.get("tags", note_put["tags"])
    
    return jsonify(search_note_request(note_id))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)