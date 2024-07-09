from flask import Flask, render_template, request
from pymongo import MongoClient

# Configure Flask app
app = Flask(__name__, static_url_path='/static')



# Replace with your actual MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "evergreen"
MONGO_COLLECTION = "sleeves"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save_data():
    name = request.form.get("name")
    age = request.form.get("age")

    if name and age:
        try:
            data = {"name": name, "age": int(age)}
            result = collection.insert_one(data)
            message = f"Successfully saved data with ID: {result.inserted_id}"
        except ValueError:
            message = "Error: Please enter a valid age (integer)."
    else:
        message = "Error: Please enter both name and age."

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
