from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

SCORE_FILE = 'scores.json'

def load_scores():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_score_to_file(score):
    scores = load_scores()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:10]  # Keep top 10
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    score = data.get('score', 0)
    save_score_to_file(score)
    return jsonify({"status": "success", "score": score})

@app.route('/get_scores')
def get_scores():
    return jsonify(load_scores())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
