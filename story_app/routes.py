
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from gtts import gTTS
from deep_translator import GoogleTranslator
import io
from . import story_bp
from flask import current_app
from story_app.models import Story,db


load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"), transport="rest")


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.7,
        "top_k": 30,
        "max_output_tokens": 700,
        "response_mime_type": "text/plain",
    }
)


@story_bp.route('/story')
def home():
    return render_template('storyform.html')


import traceback  # Add this import

@story_bp.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        data = request.json
        additional_requests = data.get('additional', '') 

        prompt = f"""
        Write a simple, easy-to-read short story for a {data.get('age', '6')}-year-old {data.get('gender', 'boy')}.
        - Mood: {data.get('mood', 'happy')}
        - Interests: {data.get('interests', 'adventure')}
        - Story Length: {data.get('story_length', 'short')}
        - Time of Day: {data.get('time_of_day', 'bedtime')}
        - Additional Requests: {additional_requests}
        The story should have:
        - A clear beginning, middle, and proper ending.
        - Simple words and short sentences.
        - No complex or abstract ideas.
        - A moral lesson or positive conclusion.
        """

        response = model.generate_content(prompt)  # <- Possible Error Point
        story = response.text if response else "Sorry, I couldn't generate a story right now."

        # Save story to database
        new_story = Story(
            age=data.get('age', 6),
            gender=data.get('gender', 'boy'),
            mood=data.get('mood', 'happy'),
            interests=data.get('interests', 'adventure'),
            story_length=data.get('story_length', 'short'),
            time_of_day=data.get('time_of_day', 'bedtime'),
            additional_data=additional_requests  
        )
        db.session.add(new_story)
        db.session.commit()

        return jsonify({'story': story})
    
    except Exception as e:
        print("Error:", str(e))  # Print the error in the console
        traceback.print_exc()  # Print full traceback for debugging
        return jsonify({'error': str(e)}), 500

@story_bp.route('/speak_story', methods=['POST'])
def speak_story():
    try:
        data = request.json
        story = data.get('story', '')
        language = data.get('language', 'en')

        if language == "hi":
            story = GoogleTranslator(source='en', target='hi').translate(story)
        elif language == "mr": 
            story = GoogleTranslator(source='en', target='mr').translate(story)

        tts = gTTS(story, lang=language)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        return Response(audio_bytes, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({'error': str(e)}), 500