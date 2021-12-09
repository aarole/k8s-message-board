from flask import Flask, request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId

DEBUG = True
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db

CORS(app, resources={r'/*': {'origins': '*'}})

def get_messages():
	messages = db.message.find()
	data = []
	for message in messages:
		item = {
			"id": str(message["_id"]),
			"name": message["name"],
			"email": message["email"],
			"message": message["message"]
		}
		data.append(item)
	data.reverse()
	return data

@app.route("/")
def index():
	messages = get_messages()
	return render_template("index.html", messages=messages)

@app.route("/messages", methods=["POST"])
def messages():
	name = request.form.get("name")
	email = request.form.get("email")
	message = request.form.get("message")
	db.message.insert_one({"name": name,"email": email, "message": message})
	return redirect(url_for("index"))

@app.route("/delete/<id>", methods=["GET"])
def delete(id):
	db.message.delete_one({"_id": ObjectId(id)})
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
