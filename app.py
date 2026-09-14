"""
Flask Web API for Voice Assistant
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from voice_assistant import VoiceAssistant

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize voice assistant
assistant = VoiceAssistant(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    google_creds_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "AI Voice Assistant API is running"})


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Transcribe audio file
    
    Expected: multipart/form-data with 'audio' file
    Returns: JSON with transcribed text
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        
        transcription = assistant.transcribe_audio(audio_data)
        return jsonify({"transcription": transcription})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    Send message to AI and get response
    
    Expected JSON: {"message": "user message"}
    Returns: JSON with AI response
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        ai_response = assistant.get_ai_response(user_message)
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/synthesize', methods=['POST'])
def synthesize():
    """
    Convert text to speech
    
    Expected JSON: {"text": "text to convert"}
    Returns: Audio file
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        text = data['text']
        audio_content = assistant.synthesize_speech(text)
        
        return audio_content, 200, {'Content-Type': 'audio/mpeg'}
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/voice-interact', methods=['POST'])
def voice_interact():
    """
    Full voice interaction: transcribe -> AI response -> synthesize
    
    Expected: multipart/form-data with 'audio' file
    Returns: JSON with transcription, response, and audio URL
    """
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        
        # Transcribe
        user_message = assistant.transcribe_audio(audio_data)
        if not user_message:
            return jsonify({"error": "Could not transcribe audio"}), 400
        
        # Get AI response
        ai_response = assistant.get_ai_response(user_message)
        
        # Synthesize speech
        speech_audio = assistant.synthesize_speech(ai_response)
        
        return jsonify({
            "transcription": user_message,
            "response": ai_response,
            "audio": speech_audio.hex()  # Return as hex string
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reset-conversation', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    assistant.conversation_history = []
    return jsonify({"status": "success", "message": "Conversation history cleared"})


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', True), port=5000)
