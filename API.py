from flask import Flask, request, jsonify
import secrets
import random
import json
import os

app = Flask(__name__)

# In-memory API key store (use a database for persistence)
api_keys = set()

# Load jokes from jokes.json file
jokes_file = "jokes.json"
if not os.path.exists(jokes_file):
    print(f"❌ ERROR: {jokes_file} not found!")
    jokes_list = []
else:
    with open(jokes_file, "r", encoding="utf-8") as f:
        try:
            jokes_list = json.load(f)
        except json.JSONDecodeError:
            print("❌ ERROR: jokes.json is not valid JSON.")
            jokes_list = []

# Route to generate API key
@app.route("/generate-key", methods=["POST"])
def generate_key():
    new_key = f"jk-{secrets.token_hex(8)}-en"
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})

# API key validation helper
def check_api_key():
    key = request.args.get("key") or request.headers.get("x-api-key")
    if not key:
        return jsonify({"error": "Missing API key"}), 401
    if key not in api_keys:
        return jsonify({"error": "Invalid API key"}), 401
    return None

# Random joke endpoint
@app.route("/jokes/random", methods=["GET"])
def random_joke():
    error = check_api_key()
    if error:
        return error

    if not jokes_list:
        return jsonify({"error": "No jokes available"}), 500

    joke_data = random.choice(jokes_list)

    # If joke is stored as {"id": 1, "joke": "..."} return only text
    if isinstance(joke_data, dict) and "joke" in joke_data:
        return jsonify({"joke": joke_data["joke"]})
    else:
        # Fallback in case jokes.json contains plain strings
        return jsonify({"joke": str(joke_data)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
