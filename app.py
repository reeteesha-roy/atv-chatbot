from flask import Flask, request, jsonify, render_template
from db import get_faqs
from matcher import find_best_match
import urllib.parse

app = Flask(__name__)

CONFIDENCE_THRESHOLD = 0.1


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({"reply": "Please enter a valid question."})

    user_input = data["message"].strip()

   
    faqs = get_faqs()
    print("FAQs:", faqs)
    for f in faqs:
        print("DB QUESTION:", repr(f.get("question")))  

    match, score = find_best_match(user_input, faqs)
   

    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "reply": match["answer"]
        })

    query = urllib.parse.quote(user_input)
    return jsonify({
    "reply": match.get("answer") or match.get("Answer") or "No answer found."})


if __name__ == "__main__":
    app.run()
