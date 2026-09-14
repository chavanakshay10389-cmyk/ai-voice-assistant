"""
Voice Assistant Core Module
Handles speech recognition, AI processing, and text-to-speech
"""
import os
from io import BytesIO
import numpy as np
from openai import OpenAI
from google.cloud import speech_v1
from google.cloud import texttospeech_v1
import pyaudio
import wave


class VoiceAssistant:
    """Main Voice Assistant class"""
    
    def __init__(self, openai_api_key, google_creds_path=None):
        """
        Initialize the Voice Assistant
        
        Args:
            openai_api_key: OpenAI API key
            google_creds_path: Path to Google Cloud credentials JSON
        """
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.speech_client = speech_v1.SpeechClient()
        self.tts_client = texttospeech_v1.TextToSpeechClient()
        self.conversation_history = []
        
        if google_creds_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds_path
    
    def record_audio(self, duration=5, sample_rate=16000):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate in Hz
            
        Returns:
            Audio data as bytes
        """
        print(f"🎙️ Recording for {duration} seconds...")
        
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024
        )
        
        frames = []
        for _ in range(0, int(sample_rate / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Convert to WAV format
        audio_buffer = BytesIO()
        with wave.open(audio_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(audio.get_sample_size(pyaudio.paFloat32))
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b"".join(frames))
        
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    
    def transcribe_audio(self, audio_data):
        """
        Convert audio to text using Google Speech-to-Text
        
        Args:
            audio_data: Audio data as bytes
            
        Returns:
            Transcribed text
        """
        print("🔄 Transcribing audio...")
        
        audio = speech_v1.RecognitionAudio(content=audio_data)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        
        response = self.speech_client.recognize(config=config, audio=audio)
        
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            print(f"📝 You said: {transcript}")
            return transcript
        else:
            print("❌ Could not understand audio")
            return ""
    
    def get_ai_response(self, user_message):
        """
        Get response from OpenAI GPT
        
        Args:
            user_message: User's message
            
        Returns:
            AI response text
        """
        print("🤖 Processing with AI...")
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=150
        )
        
        ai_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_message
        })
        
        print(f"🤖 AI: {ai_message}")
        return ai_message
    
    def synthesize_speech(self, text):
        """
        Convert text to speech using Google Text-to-Speech
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio content as bytes
        """
        print("🔊 Generating speech...")
        
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-C",
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )
        
        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config,
        )
        
        return response.audio_content
    
    def play_audio(self, audio_content):
        """
        Play audio content
        
        Args:
            audio_content: Audio data as bytes
        """
        print("🎵 Playing response...")
        # Implementation depends on audio format and OS
        # This is a placeholder for audio playback
        pass
    
    def listen_and_respond(self):
        """
        Main loop: listen for audio, process, and respond
        """
        try:
            # Record audio from user
            audio_data = self.record_audio(duration=5)
            
            # Transcribe audio
            user_message = self.transcribe_audio(audio_data)
            if not user_message:
                return
            
            # Get AI response
            ai_response = self.get_ai_response(user_message)
            
            # Synthesize and play response
            speech_audio = self.synthesize_speech(ai_response)
            self.play_audio(speech_audio)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
