from flask import Flask, request, jsonify, render_template
from db import faq_collection
from matcher import find_best_match
import urllib.parse

app = Flask(__name__)

CONFIDENCE_THRESHOLD = 0.25


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"reply": "Please enter a valid question."})

    user_input = data["message"].strip()

    match, score = find_best_match(user_input, faq_collection)

    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "reply": match["answer"]
        })

    query = urllib.parse.quote(user_input)
    return jsonify({
        "reply": "I may not have the exact information for that.",
        "link": f"https://www.google.com/search?q=ATV+{query}"
    })


if __name__ == "__main__":
    app.run()
