from flask import Flask, jsonify
import json
import random

app = Flask(__name__)

with open("jokes.json", "r", encoding="utf-8") as f:
    jokes = json.load(f)

@app.route("/jokes/random")
def random_joke():
    joke = random.choice(jokes)
    return jsonify(joke)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
