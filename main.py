from flask import Flask, jsonify
import json
import random
import os

app = Flask(__name__)

jokes_file = "jokes.json"

if not os.path.exists(jokes_file):
    print(f"ERROR: {jokes_file} not found!")
    jokes = []
else:
    with open(jokes_file, "r", encoding="utf-8") as f:
        try:
            jokes = json.load(f)
            print(f"Loaded {len(jokes)} jokes")
        except Exception as e:
            print(f"Error loading JSON: {e}")
            jokes = []

@app.route("/jokes/random")
def random_joke():
    if not jokes:
        return jsonify({"error": "No jokes available"}), 500
    joke = random.choice(jokes)
    return jsonify(joke)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
