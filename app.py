from flask import Flask, jsonify, abort, make_response, request
from init_db import *
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)


# Доделать put-запрос +
# Решить проблему с id, если нет (отсоритировать по убыванию и первый последний)
# Исправить тесты
# модель базы, в тегах список внутри строки +
# Переписать ВСЕ ЗАПИСИ +
# Переписать Создание +
# Переписать ИЗМЕНЕНИЕ +
# Переписать Удаление +


# Все записи
@app.route("/notes/api/notes", methods=["GET"])
def get_notes():
    query = Note.select()
    all_notes = []
    for i in query:
        note_json = model_to_dict(i)
        tags = (Tag
                .select()
                .join(TagNote)
                .where(TagNote.note == i.id))
        tags_of_note = []

        for tag in tags:
            tags_of_note.append(tag.tag)

        note_json['tags']=tags_of_note
        all_notes.append(note_json)
        
    return jsonify(all_notes)


# Отдельная запись
@app.route("/notes/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = Note.get(Note.id == note_id)
    if note.id == note_id:
        tags = (Tag
            .select()
            .join(TagNote)
            .where(TagNote.note == note_id))
        
        tags_of_note = []
        for tag in tags:
            tags_of_note.append(tag.tag)
    else:
        abort(404)

    return jsonify({"id": note.id, "title": note.title, "text": note.text, "tags": tags_of_note})
    

# Удаление записи
@app.route("/notes/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note_d = Note.get(Note.id == note_id)
    note_d.delete_instance()

    tag_note_delete = TagNote.delete().where(TagNote.note == note_id)
    tag_note_delete.execute()

    return jsonify({"result": True})


# Создание записи
@app.route("/notes/api/notes", methods=["POST"])
def create_note():
    if not request.json or not "title" in request.json:
        abort(400)

    note_post = {
        "title": request.json["title"],
        "text": request.json.get("text", ""),
        "tags": request.json.get("tags", "")
    }
    
    new_note = Note.create(title=note_post["title"], text=note_post["text"])
    # Работа с тегами
    data = note_post['tags']
    for i in data:
        try:
            tag = Tag.get(Tag.tag == i)
            TagNote.create(note=new_note.id, tag=tag.id)
        except Tag.DoesNotExist:
            tag = Tag.create(tag=i)
            TagNote.create(note=new_note.id, tag=tag.id)
    
    return jsonify(note_post), 201


# Изменение записи ++++
@app.route("/notes/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    if not request.json:
        abort(400)
    
    note_put = {
        "title": request.json["title"],
        "text": request.json.get("text", ""),
        "tags": request.json.get("tags", "")
    }

    new_note = Note(title=note_put["title"], text=note_put["text"])
    new_note.id = note_id
    new_note.save()
    
    # Работа с тегами
    data = note_put['tags']
    tag_note_delete = TagNote.delete().where(TagNote.note == note_id)
    tag_note_delete.execute()

    for i in data:
        try:
            tag = Tag.get(Tag.tag == i)
            TagNote.create(note=new_note.id, tag=tag.id)
        except Tag.DoesNotExist:
            tag = Tag.create(tag=i)
            TagNote.create(note=new_note.id, tag=tag.id)
    

    return jsonify(note_put)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)