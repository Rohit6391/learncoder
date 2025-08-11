from flask import Flask, request, jsonify
import secrets
import random
import json
import os

app = Flask(__name__)

# Files to store API keys and jokes
API_KEYS_FILE = "api_keys.txt"
JOKES_FILE = "jokes.json"

# Load existing API keys from file or create empty set
if os.path.exists(API_KEYS_FILE):
    with open(API_KEYS_FILE, "r") as f:
        api_keys = set(line.strip() for line in f.readlines() if line.strip())
else:
    api_keys = set()

# Load jokes from JSON file
with open(JOKES_FILE, "r", encoding="utf-8") as f:
    jokes_list = json.load(f)

def save_api_keys():
    with open(API_KEYS_FILE, "w") as f:
        for key in api_keys:
            f.write(key + "\n")

@app.route("/generate-key", methods=["POST"])
def generate_key():
    new_key = "jk-" + secrets.token_hex(8) + "-en"
    api_keys.add(new_key)
    save_api_keys()
    return jsonify({"api_key": new_key})

def check_api_key():
    key = request.args.get("key") or request.headers.get("x-api-key")
    if not key or key not in api_keys:
        return jsonify({"error": "Invalid or missing API key"}), 401
    return None

@app.route("/jokes/random", methods=["GET"])
def random_joke():
    error_response = check_api_key()
    if error_response:
        return error_response
    joke = random.choice(jokes_list)
    # If joke is a dict, extract "joke" text (based on your jokes.json format)
    if isinstance(joke, dict) and "joke" in joke:
        joke_text = joke["joke"]
    else:
        joke_text = str(joke)
    return jsonify({"joke": joke_text})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Joke API running. Use /generate-key (POST) to get API key, then /jokes/random?key=YOUR_KEY"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
