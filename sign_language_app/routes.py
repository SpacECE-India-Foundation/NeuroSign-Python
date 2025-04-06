<<<<<<< HEAD
from flask import Flask, render_template, request, url_for, jsonify, send_file
import os
import cv2
import mediapipe as mp #pretrained model for ASL
import base64
import numpy as np
import time
import google.generativeai as genai
from googletrans import Translator
from gtts import gTTS
import uuid
import asyncio
from googletrans import Translator
from . import sign_language_bp


genai.configure(api_key="AIzaSyC-AublNqOvjvJ5zMNj9gDKoEgagDwU85g")

# Paths for ASL and ISL image folders
ASL_PATH = "static/ASL"
ISL_PATH = "static/ISL"
DETECTED_TEXT=''
WL=[]
AF=''
LANGUAGES = {
    'hi': 'Hindi',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'te': 'Telugu',
    'ta': 'Tamil',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'en': 'English'
}

#functions for sttring processing
def compress_string(s, threshold=20):
    compressed = ""
    i = 0
    while i < len(s):
        count = 1
        while i + 1 < len(s) and s[i] == s[i + 1]:  # Count consecutive occurrences
            count += 1
            i += 1
        if count >= threshold:  # Only include if count meets the threshold
            compressed += s[i]
        i += 1
    return compressed



##################
#prediction
##################
import nltk
from nltk.corpus import words
nltk.download("words")
word_list = words.words()
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.words = [] 
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the Trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.words.append(word) 
        node.is_end_of_word = True

    def autocomplete(self, prefix):
        """Return all words that start with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return [] 
            node = node.children[char]
        return sorted(set(node.words))  
trie = Trie()
for w in word_list:
    trie.insert(w)
###########################################################3


# Function to translate text into sign language images
def get_sign_language_images(text, language):
    folder_path = ASL_PATH if language == "ASL" else ISL_PATH
    images = []
    for letter in text.lower():
        if letter.isalpha() or letter.isdigit():
            image_filename = f"{letter}.jpg"
            image_path = os.path.join(folder_path, image_filename)
            if os.path.exists(image_path):
                image_url = url_for('static', filename=f"{language.upper()}/{image_filename}")
                images.append(image_url)
            else:
                images.append(url_for('static', filename="placeholder.jpg"))
    return images

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Global variable to store detected gesture
recognizer_detected = None

# Output function for gesture recognition
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global recognizer_detected
    if result.gestures and len(result.gestures) > 0 and len(result.gestures[0]) > 0:
        recognizer_detected = result.gestures[0][0].category_name
        print('Gesture Recognition Result:', recognizer_detected)
    else:
        recognizer_detected = None

# Setting options for gesture recognition
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='sign_language_app/exported_models/gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

recognizer = GestureRecognizer.create_from_options(options)




=======
from flask import render_template, request, jsonify, url_for
import os
import cv2
import mediapipe as mp
import base64
import numpy as np
import time
from . import sign_language_bp

ASL_PATH = "static/ASL"
ISL_PATH = "static/ISL"
DETECTED_TEXT = ''

def get_sign_language_images(text, language):
    folder_path = ASL_PATH if language == "ASL" else ISL_PATH
    images = [url_for('static', filename=f"{language.upper()}/{letter}.jpg") 
              if os.path.exists(os.path.join(folder_path, f"{letter}.jpg")) else url_for('static', filename="placeholder.jpg")
              for letter in text.lower() if letter.isalpha() or letter.isdigit()]
    return images

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
recognizer_detected = None

>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf
@sign_language_bp.route('/sign_language')
def sign_language_home():
    return render_template('home.html')

@sign_language_bp.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return render_template('trans.html')

    # Handle POST request
    text_input = request.form.get("text_input")
    speech_input = request.form.get("speech_input")
    language_choice = request.form.get("language")

    input_text = text_input if text_input else speech_input

    if input_text:
        images = get_sign_language_images(input_text, language_choice)
        return render_template('trans.html', images=images, input_text=input_text, language=language_choice)

    return render_template('trans.html', images=None)

<<<<<<< HEAD
lr=''
count=0



@sign_language_bp.route('/process_frame', methods=['GET','POST'])
def process_frame():
    global DETECTED_TEXT,lr,count
=======
@sign_language_bp.route('/process_frame', methods=['GET','POST'])
def process_frame():
    global DETECTED_TEXT
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf
    if request.method == 'GET':
        return render_template('index.html')
    global recognizer_detected
    frame_timestamp_ms = int(time.time() * 1000)
<<<<<<< HEAD
    print(frame_timestamp_ms)
=======
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf

    # Get the image data from the request
    data = request.json
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)

    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process the frame for gesture recognition
    recognizer.recognize_async(mp_image, frame_timestamp_ms)

    # Process hand landmarks
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display recognized gesture on the frame
<<<<<<< HEAD
        #adding a bit of delay to ensure proper detection
    if recognizer_detected:
        if not lr:
            lr = recognizer_detected
            count+=1
        elif lr == recognizer_detected:
            count+=1
        elif lr!=recognizer_detected:
            lr=recognizer_detected
            count=1
        if count >= 20:
            cv2.putText(frame, recognizer_detected, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, recognizer_detected, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv2.LINE_AA)    
=======
    if recognizer_detected:
        cv2.putText(frame, recognizer_detected, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf
        DETECTED_TEXT=DETECTED_TEXT+recognizer_detected

    # Encode processed image for response
    ret, buffer = cv2.imencode('.jpg', frame)
    processed_image = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify(result=recognizer_detected, image='data:image/jpeg;base64,' + processed_image)

<<<<<<< HEAD
#this routes resets the values to default
@sign_language_bp.route('/reset', methods=['POST'])
def reset():
    global WL,DETECTED_TEXT
    WL=[]
    DETECTED_TEXT=""
    return jsonify(response="reset done")

#this route will display autocomplete output in real-time 
@sign_language_bp.route('/autocomplete', methods=['POST'])
def P_text():
    global DETECTED_TEXT, WL
    if len(DETECTED_TEXT) > 0:
        WL = trie.autocomplete(compress_string(DETECTED_TEXT))
        return jsonify(prediction=WL if len(WL) >=1 else ["no similar word found"])
    else:
        return jsonify(prediction="No gestures recognized")


#route for sentence using gen-ai
@sign_language_bp.route('/predict', methods=['POST'])
async def predict():  
    try:
        data = request.json
        recognized_words = data.get("words", [])
        lang_code = data.get("lang", "en")

        if not recognized_words:
            return jsonify({"error": "No words provided"}), 400

        # Generate a meaningful sentence using Gemini
        prompt = f"Create a short, natural-sounding sentence using the word(s): {', '.join(recognized_words)}. The sentence should be meaningful, casual, and easy to read. Avoid special characters and formatting. Keep it simple and relevant to the given words."

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        # Check if response is valid
        if not hasattr(response, "text"):
            raise ValueError("Invalid response from Gemini")

        sentence = response.text.strip()
        print(f"Generated Sentence: {sentence}")

        # Use sync translator to avoid async issues
        translator = Translator()
        translated = translator.translate(sentence, src='en', dest=lang_code)
        translated_text = translated.text
        print(f"Translated Sentence: {translated_text}")


        audio_dir = "temp_audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)


        # Generate audio file
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("temp_audio", filename)  # Ensure the correct path

        tts = gTTS(text=translated_text, lang=lang_code)
        tts.save(filepath)

        return jsonify({"sentence": sentence, "translated": translated_text, "audio": filename})

    except Exception as e:
        print(f"Error in /predict: {e}")
        return jsonify({"error": str(e)}), 500



@sign_language_bp.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    try:
        filepath = os.path.join("temp_audio", filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        response = send_file(filepath, mimetype="audio/mpeg")

        def cleanup():
            if os.path.exists(filepath):
                os.remove(filepath)

        response.call_on_close(cleanup)
        return response
    except Exception as e:
        print("Error in /audio:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500
    try:
        global AF
        AF = filename  # Ensure the correct file path
        response = send_file(AF, mimetype="audio/mpeg")

        # Define cleanup function correctly
        def cleanup():
            print("inside clean")
            global AF
            if os.path.exists(AF):
                os.remove(AF)  # Delete file after sending

        response.call_on_close(cleanup)  # Register cleanup function properly
        response.direct_passthrough = False
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
=======
@sign_language_bp.route('/predict', methods=['POST'])
def P_text():
    global DETECTED_TEXT
    if len(DETECTED_TEXT) > 0:
        temp = DETECTED_TEXT
        DETECTED_TEXT=''
        temp=predict_sentence(temp)
        print(temp)
        return jsonify(prediction=temp)
    else:
        return jsonify(prediction="No gestures recognized")
>>>>>>> 1038ca7102254afc462e6b46760820e902cbe2bf
