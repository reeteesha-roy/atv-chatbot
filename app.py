from flask import Flask, request, jsonify
from db import faq_collection
from matcher import find_best_match
import urllib.parse

app = Flask(__name__)

CONFIDENCE_THRESHOLD = 0.25


@app.route("/", methods=["GET"])
def home():
    return "🤖 ATV Support Chatbot backend is running."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a valid question."})

    match, score = find_best_match(user_input, faq_collection)

    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "reply": match["answer"],
            "confidence": score
        })
    else:
        query = urllib.parse.quote(user_input)
        return jsonify({
            "reply": "I may not have the exact information for that.",
            "learn_more": f"https://www.google.com/search?q=ATV+{query}",
            "confidence": score
        })


if __name__ == "__main__":
    app.run(debug=True)
