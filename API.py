from flask import Flask, request, jsonify
import secrets
import random
import json

app = Flask(__name__)

# In-memory API key store (replace with DB for production)
api_keys = set()

# Load jokes from jokes.json file
with open("jokes.json", "r", encoding="utf-8") as f:
    jokes_list = json.load(f)

# Route to generate API key
@app.route("/generate-key", methods=["POST"])
def generate_key():
    new_key = "jk-" + secrets.token_hex(8) + "-en"
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})

# Middleware-like function to check API key
def check_api_key():
    key = request.args.get("key") or request.headers.get("x-api-key")
    if not key or key not in api_keys:
        return jsonify({"error": "Invalid or missing API key"}), 401
    return None

# Random joke endpoint
@app.route("/jokes/random", methods=["GET"])
def random_joke():
    error = check_api_key()
    if error:
        return error
    return jsonify({"joke": random.choice(jokes_list)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
