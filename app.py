from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from db import faq_collection
from matcher import find_best_match
import urllib.parse

app = Flask(__name__)
CORS(app)  

CONFIDENCE_THRESHOLD = 0.25


@app.route("/", methods=["GET"])
def home():
    return send_file("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("query", "").strip()  

    if not user_input:
        return jsonify({
            "answer": "Please enter a valid question.",
            "category": "General Inquiry"
        })

    match, score = find_best_match(user_input, faq_collection)

    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "answer": match["answer"],
            "category": match.get("category", "General Inquiry"),
            "confidence": score
        })
    else:
        query = urllib.parse.quote(user_input)
        return jsonify({
            "answer": f"I may not have the exact information for that. You can learn more here: https://www.google.com/search?q=ATV+{query}",
            "category": "General Inquiry",
            "confidence": score
        })


if __name__ == "__main__":
    app.run(debug=True)
