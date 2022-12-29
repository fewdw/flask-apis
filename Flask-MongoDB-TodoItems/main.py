import pymongo as pymongo
from flask import Flask, request, jsonify
from flask_objectid_converter import ObjectIDConverter
from pymongo import ReturnDocument
from pymongo.server_api import ServerApi
from Schemas import ToDoItemSchemaPut, ToDoItemSchemaPost, ToDoItemsSchemaPatch
from bson import json_util, ObjectId
from flask_cors import CORS

#loading private connection information from environment variables
from dotenv import load_dotenv
load_dotenv()
import os
MONGODB_LINK = os.environ.get("MONGODB_LINK")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASS = os.environ.get("MONGODB_PASS")

#connecting to mongodb
client = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_LINK}/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#name of database
db = client.todoitem_sec1

app = Flask(__name__)
#adding an objectid type for the URL fields instead of treating it as string
#this is coming from a library we are using instead of building our own custom type
app.url_map.converters['objectid'] = ObjectIDConverter

app.config['DEBUG'] = True
#making our API accessible by any IP
CORS(app)

@app.route("/users/<user_id>/todos", methods=["POST"])
def add_new_todo_item(user_id):
    error = ToDoItemSchemaPost().validate(request.json)
    if error:
        return error, 400
    todo_data = {'complete': False, 'user_id':user_id}
    todo_data.update(request.json)
    try:
        inserted_id = db.todos.insert_one(todo_data).inserted_id
        todo_data["_id"] = str(inserted_id)
        return jsonify(todo_data)

    except Exception as e:
        return {"error": "some error happened"}, 500

@app.route("/users/<user_id>/todos", methods=["GET"])
def get_all_todos(user_id):
    try:
        cursor = db.todos.find({"user_id": user_id})
        todos = list(cursor)
        for todo in todos:
            if "_id" in todo:
                todo["_id"] = str(todo["_id"])

        return jsonify(todos)
    except Exception as e:
        print(e)
        return {"error": "some error happened"}, 501

#notice that todo_id is of type objectid.. not any string is accepted
@app.route("/users/<user_id>/todos/<objectid:todo_id>", methods=["PUT", "PATCH"])
def update_todo_item(user_id, todo_id):
    error = {}
    if request.method == 'PUT':
        error = ToDoItemSchemaPut().validate(request.json)
    elif request.method == 'PATCH':
        error = ToDoItemsSchemaPatch().validate(request.json)

    if error:
        return error, 400
    try:
        updated_todo_item = db.todos.find_one_and_update({"user_id":user_id, "_id": ObjectId(todo_id)},
                                     {"$set": request.json},
                                     return_document=ReturnDocument.AFTER, upsert=False)

        if updated_todo_item is None:
            return {"error": "resource not found"}, 404

        if "_id" in updated_todo_item:
            updated_todo_item["_id"] = str(updated_todo_item["_id"])
        return updated_todo_item

    except Exception as e:
        return {"error": "some error happened"}, 501

@app.route("/users/<user_id>/todos/<objectid:todo_id>", methods=["DELETE"])
def delete_todo_item(user_id, todo_id):

    try:
        deleted_item = db.todos.find_one_and_delete({"user_id": user_id, "_id":ObjectId(todo_id)},
                                                    projection={"_id":False})
        if deleted_item is None:
            return {"error": "resource not found"}, 404
        if "_id" in deleted_item:
            deleted_item["_id"] = str(deleted_item["_id"])

        return jsonify(deleted_item)

    except Exception as e:
        return {"error": "some error happened"}, 501

if __name__ == "__main__":
    app.run(port=5002)
