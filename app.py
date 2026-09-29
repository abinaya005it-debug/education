from flask import Flask, render_template, request, jsonify
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

app = Flask(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """ You are EduBot, an Education Domain AI Assistant.

Answer ONLY questions related to education and academic learning.

Educational questions include:
- School and college subjects
- Mathematics, Physics, Chemistry, Biology
- Computer Science
- Artificial Intelligence and Data Science
- Programming
- Data Structures and Algorithms
- Operating Systems
- Computer Networks
- DBMS
- Engineering subjects
- Exams, assignments, projects and study-related questions

If the question is NOT related to education, do not answer it.

For non-educational questions, reply exactly:
This question is not related to education. Please ask an education-related question.

If a general topic is clearly asked for an academic purpose, you may answer it.

For educational questions, give a clear and student-friendly answer.."""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a question."})

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nStudent question: {message}"
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        reply = getattr(response, "text", None) or "I couldn't generate a response."
        return jsonify({"reply": reply})
    except Exception as e:
        print("Gemini error:", e)
        return jsonify({
            "reply": "Sorry, I couldn't process your question. Please check your API key and try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
