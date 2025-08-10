from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import string

app = Flask(__name__)
CORS(app, origins=["https://neurajoke.netlify.app"])  # Allow your frontend domain

# Load jokes
with open("jokes.json", "r", encoding="utf-8") as f:
    jokes = json.load(f)

# In-memory API keys storage (replace with DB for real apps)
api_keys = set()

def generate_api_key():
    # Generate a random key like: jk-ab12cd34ef56
    return "jk-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12))

@app.route("/get_api_key", methods=["GET"])
def get_api_key():
    new_key = generate_api_key()
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})

def valid_api_key(key):
    return key in api_keys

@app.route("/jokes/random", methods=["GET"])
def random_joke():
    key = request.args.get("key", "")
    if not valid_api_key(key):
        return jsonify({"error": "Invalid or missing API key"}), 403
    return jsonify(random.choice(jokes))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
