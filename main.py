from flask import Flask, jsonify, render_template, request
import json
import random
import string

app = Flask(__name__)

# Your website domain allowed without API key
ALLOWED_WEBSITE_DOMAIN = "neurajoke.netlify.app"

# Load jokes
with open("jokes.json", "r", encoding="utf-8") as f:
    jokes = json.load(f)

# In-memory storage for API keys (use a database for real app)
api_keys = set()

def generate_api_key():
    return "jk-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=12)) + "-en"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_api_key", methods=["GET"])
def get_api_key():
    new_key = generate_api_key()
    api_keys.add(new_key)
    return jsonify({"api_key": new_key})

def is_allowed_without_key():
    referer = request.headers.get("Referer", "")
    if ALLOWED_WEBSITE_DOMAIN in referer:
        return True
    return False

def valid_api_key():
    key = request.args.get("key", "")
    return key in api_keys

@app.route("/jokes/random", methods=["GET"])
def random_joke():
    if is_allowed_without_key() or valid_api_key():
        return jsonify(random.choice(jokes))
    return jsonify({"error": "Invalid or missing API key"}), 403

@app.route("/jokes", methods=["GET"])
def all_jokes():
    if is_allowed_without_key() or valid_api_key():
        return jsonify(jokes)
    return jsonify({"error": "Invalid or missing API key"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
