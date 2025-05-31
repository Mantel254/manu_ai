from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Route: home page
@app.route('/')
def home():
    return render_template('index.html')

# Route: chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'reply': "Pole, sijaelewa. Jaribu tena."})

    # Set up headers for Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Chat payload
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are manu.ai, a witty Kenyan chatbot that speaks Swahili and English. "
                    "You were built by a Kenyan student in just a few hours. Respond informally, briefly, "
                    "and with Kenyan cultural flavor (e.g., use 'sasa', 'ah buda', 'uko aje')."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content'].strip()
        return jsonify({'reply': reply})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({'reply': "Manu.ai anakazana lakini kuna network error. Try tena baadaye."}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
