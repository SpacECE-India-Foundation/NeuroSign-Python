import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("API_KEY"), transport="rest")

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 1.2,  # Slightly creative
        "top_p": 0.95,
        "top_k": 50,
        "max_output_tokens": 1024,
        "response_mime_type": "text/plain",
    }
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.json
    age = data.get('age', '6')  # Default to 6 years old
    gender = data.get('gender', 'neutral')
    mood = data.get('mood', 'happy')
    interests = data.get('interests', 'adventure')
    character = data.get('character', 'a kind kid')
    time_of_day = data.get('time_of_day', 'bedtime')
    additional = data.get('additional', '')

    prompt = f"""
    Create a short story for a {age}-year-old {gender} child.
    Mood: {mood}
    Interests: {interests}
    Main character: {character}
    Time of day: {time_of_day}
    Additional requests: {additional}

    Make it engaging, easy to understand, and fun!
    """

    response = model.generate_content(prompt)
    story = response.text if response else "Sorry, I couldn't generate a story right now."

    return jsonify({'story': story})

if __name__ == '__main__':
    app.run(debug=True)
