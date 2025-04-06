## Installation

1. **Clone the repository:**

   git clone https://github.com/DiyaBhujbal/NeuroSignAndSenseIQ.git . (some folder)
=======
   git clone https://github.com/gesture_recognition.git . (some folder)

=======
   git clone https://github.com/gesture_recognition.git . (some folder)

   cd (folder name)

2. **Create a virtual environment:**

   python3 -m venv neurosign

   source neurosign/bin/activate  # Linux/Mac
   neurosign\Scripts\activate     # Windows
=======
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

=======
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows


3. **Install dependencies:**

   pip install -r requirements.txt

4. **Set up the API Key:**
   - Replace `api_key` in `predict_sentence` function with your Google Gemini API key.

## Running the Project

1. **Start the Flask server:**

   python app.py

2. **Open the application in your browser:**
   
   http://127.0.0.1:5000
   
