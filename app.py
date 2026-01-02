from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from db import faq_collection
from matcher import find_best_match
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

CONFIDENCE_THRESHOLD = 0.5  

def get_context_from_db():
    """Get all FAQs to provide context to Gemini"""
    faqs = list(faq_collection.find({}, {"_id": 0, "question": 1, "answer": 1}))
    context = "Here is our FAQ knowledge base:\n\n"
    for i, faq in enumerate(faqs, 1):
        context += f"{i}. Q: {faq['question']}\n   A: {faq['answer']}\n\n"
    return context


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("query", "").strip()

    if not user_input:
        return jsonify({
            "answer": "Please enter a valid question.",
            "category": "General"
        })

  
    match, score = find_best_match(user_input, faq_collection)
    if match and score >= CONFIDENCE_THRESHOLD:
        return jsonify({
            "answer": match["answer"],
            "category": match.get("category", "General"),
            "source": "database",
            "confidence": score
        })
    
    try:
        context = get_context_from_db()
        
        prompt = f"""{context}
You are an expert assistant for Team Garvit's ATV products and services.Based on the FAQ knowledge base above, please answer the following user question. If the answer is in the FAQ, provide that information. 
If not, suggest they contact support for specific details.
Do NOT use outside knowledge. Do NOT guess or assume.
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
        
        if match:
            return jsonify({
                "answer": match["answer"],
                "category": match.get("category", "General"),
                "source": "database_fallback",
                "confidence": score
            })
        return jsonify({
            "answer": "I'm having trouble processing your question right now. Please try rephrasing or contact our support team.",
            "category": "General",
            "source": "fallback"
        })


if __name__ == "__main__":
    app.run(debug=True)






