from flask import Flask, jsonify
import json
import random

app = Flask(__name__)

# Load jokes from jokes.json
with open('jokes.json', 'r', encoding='utf-8') as f:
    jokes = json.load(f)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Joke API! Endpoints: /jokes, /joke/random"})

@app.route('/jokes', methods=['GET'])
def get_jokes():
    return jsonify(jokes)

@app.route('/joke/random', methods=['GET'])
def get_random_joke():
    return jsonify(random.choice(jokes))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
