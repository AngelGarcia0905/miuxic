import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allows your website to communicate with this server
CORS(app)

# Load the API Key safely
api_key = os.environ.get("AIzaSyB9yH2o8e0d6cyzepXJVpKgqX8yJ678c2k")
if api_key:
    genai.configure(api_key=api_key)

# Using the pro model for better audio analysis
model = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/', methods=['GET'])
def home():
    """Simple check to see if the server is awake"""
    return jsonify({"status": "online", "message": "miuxic API is running"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Receives audio and returns ABC musical notation"""
    try:
        # Check if the file is in the request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400
            
        audio_file = request.files['audio']
        
        # Save temporarily
        audio_path = "temp_audio.mp3"
        audio_file.save(audio_path)
        
        # Upload and process
        uploaded_file = genai.upload_file(path=audio_path)
        
        prompt = """
        Listen to this audio and transcribe the melody to ABC Musical Notation.
        Output ONLY the ABC code, starting with X:1. 
        Do not add any explanations or extra text.
        """
        
        response = model.generate_content([prompt, uploaded_file])
        
        # Delete temporary file
        os.remove(audio_path)
        
        return jsonify({
            "status": "success",
            "abc_code": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
