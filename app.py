from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from db import faq_collection
from matcher import find_best_match
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

CONFIDENCE_THRESHOLD = 0.5  # Increased threshold


def get_context_from_db():
    """Get all FAQs to provide context to Gemini"""
    faqs = list(faq_collection.find({}, {"_id": 0, "question": 1, "answer": 1}))
    context = "Here is our FAQ knowledge base:\n\n"
    for i, faq in enumerate(faqs, 1):
        context += f"{i}. Q: {faq['question']}\n   A: {faq['answer']}\n\n"
    return context


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
            "category": "General"
        })

    # First, try to find exact match in database
    match, score = find_best_match(user_input, faq_collection)

    # If high confidence match, use database answer
    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "answer": match["answer"],
            "category": match.get("category", "General"),
            "source": "database",
            "confidence": score
        })
    
    # Otherwise, use Gemini with FAQ context
    try:
        context = get_context_from_db()
        
        prompt = f"""{context}
You are an expert assistant for Team Garvit's ATV products and services.Based on the FAQ knowledge base above, please answer the following user question. If the answer is in the FAQ, provide that information. 
If not, provide a helpful and informative response regarding this topic and suggest they contact support for specific details.

User Question: {user_input}

Answer (be concise and helpful):"""

        response = model.generate_content(prompt)
        
        return jsonify({
            "answer": response.text,
            "category": "General",
            "source": "gemini",
            "confidence": 0.8
        })
    
    except Exception as e:
        print(f"Gemini API Error: {e}")
        
        # Fallback to database answer if Gemini fails
        if match:
            return jsonify({
                "answer": match["answer"],
                "category": match.get("category", "General"),
                "source": "database_fallback",
                "confidence": score
            })
        
        # Ultimate fallback
        return jsonify({
            "answer": "I'm having trouble processing your question right now. Please try rephrasing or contact our support team.",
            "category": "General",
            "source": "fallback"
        })


if __name__ == "__main__":
    app.run(debug=True)

