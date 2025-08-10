from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json
import random
import secrets

app = Flask(__name__)
CORS(app)

with open("jokes.json", "r", encoding="utf-8") as f:
    jokes = json.load(f)

api_keys = set()

@app.route("/generate-api-key", methods=["POST"])
def generate_api_key():
    new_key = secrets.token_hex(16)
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})

def require_api_key(func):
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if not key or key not in api_keys:
            return jsonify({"error": "Missing or invalid API key"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/jokes/random")
@require_api_key
def random_joke():
    joke = random.choice(jokes)
    return jsonify(joke)

@app.route("/jokes/<int:joke_id>")
@require_api_key
def joke_by_id(joke_id):
    # Assuming jokes have an 'id' field, find joke with that id
    joke = next((j for j in jokes if j.get("id") == joke_id), None)
    if joke is None:
        return jsonify({"error": "Joke not found"}), 404
    return jsonify(joke)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
