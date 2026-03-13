from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["POST"])
def signup():

    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("INSERT INTO users(username,password) VALUES(?,?)",
              (username,password))

    conn.commit()
    conn.close()

    return jsonify({"message":"Signup successful"})


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username,password))

    user = c.fetchone()

    conn.close()

    if user:
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})


# ---------------- PLANT DATABASE ----------------

plants = {

    "tulsi":{
        "scientific":"Ocimum tenuiflorum",
        "description":"Tulsi is a sacred medicinal herb widely used in Ayurveda.",
        "medicine":"Boosts immunity, treats cold, cough and respiratory problems."
    },

    "neem":{
        "scientific":"Azadirachta indica",
        "description":"Neem is a powerful medicinal tree used in traditional medicine.",
        "medicine":"Antibacterial, treats skin diseases, improves oral health."
    },

    "aloe":{
        "scientific":"Aloe vera",
        "description":"Aloe vera is a succulent plant known for healing gel.",
        "medicine":"Used for burns, skin care, digestion and immunity."
    }

}


# ---------------- SIMPLE IMAGE DETECTION ----------------
# (Dummy logic for demo, replace with ML later)

def detect_plant(filename):

    key = random.choice(list(plants.keys()))
    return plants[key]


# ---------------- IMAGE UPLOAD + PREDICT ----------------

@app.route("/predict", methods=["POST"])
def predict():

    image = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(path)

    plant = detect_plant(image.filename)

    return jsonify({
        "scientific_name":plant["scientific"],
        "description":plant["description"],
        "medicinal_value":plant["medicine"]
    })


# --------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
