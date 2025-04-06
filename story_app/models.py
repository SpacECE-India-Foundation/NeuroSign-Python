from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mood = db.Column(db.String(50), nullable=True)
    interests = db.Column(db.String(100), nullable=True)
    story_length = db.Column(db.String(50), nullable=True)
    time_of_day = db.Column(db.String(50), nullable=True)
    additional_data = db.Column(db.String(150), nullable=True)  
