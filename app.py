from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # or paste your key directly, not recommended

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "No question provided."})

    # Talk to Groq API
    try:
        groq_response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are a helpful tutor for math and computer science students."},
                    {"role": "user", "content": f"Walk through the steps on how to solve this problem: {question}"}
                ],
                "temperature": 0.4
            }
        )
        groq_data = groq_response.json()
        answer = groq_data["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

