from flask import Flask, render_template
<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai
from flask_cors import CORS
from dyslexia_app import dyslexia_bp
from sign_language_app import sign_language_bp
from hobby_prediction_app import hobby_prediction_bp
from story_app import story_bp  # Import the function to get the blueprint



import os

app = Flask(__name__)
app.secret_key = 'secret_key'

CORS(app)
CORS(dyslexia_bp)  
CORS(story_bp) 


# Set up upload folder and extensions
app.config['UPLOAD_FOLDER'] = 'uploads/'  
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif'}
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from story_app.models import db  # Import db after app is created

db.init_app(app)  # Initialize the database with the app

with app.app_context():
    db.create_all()  # Create tables


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


# class Story(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     age = db.Column(db.Integer, nullable=False)
#     gender = db.Column(db.String(10), nullable=False)
#     mood = db.Column(db.String(50), nullable=True)
#     interests = db.Column(db.String(100), nullable=True)
#     story_length = db.Column(db.String(50), nullable=True)
#     time_of_day = db.Column(db.String(50), nullable=True)
#     additional_data = db.Column(db.String(150), nullable=True)  


# with app.app_context():
#     db.create_all()

app.register_blueprint(dyslexia_bp)
app.register_blueprint(sign_language_bp)
app.register_blueprint(hobby_prediction_bp)
app.register_blueprint(story_bp)  # Register the new story blueprint

=======
from dyslexia_app import dyslexia_bp
from sign_language_app import sign_language_bp

app = Flask(__name__)
app.register_blueprint(dyslexia_bp)
app.register_blueprint(sign_language_bp)
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf

@app.route('/')
def home():
    return render_template('mainpage.html')

if __name__ == '__main__':
<<<<<<< HEAD
    os.makedirs('uploads', exist_ok=True)
=======
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf
    app.run(debug=True)
