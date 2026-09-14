"""
AI Voice Assistant - Main Application
"""
import os
import sys
from dotenv import load_dotenv
from voice_assistant import VoiceAssistant

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the voice assistant"""
    print("🎤 Initializing AI Voice Assistant...")
    
    assistant = VoiceAssistant(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        google_creds_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    
    print("✅ Voice Assistant Ready!")
    print("Commands:")
    print("  'listen' - Start listening for voice input")
    print("  'exit' - Quit the application\n")
    
    while True:
        user_input = input("Enter command: ").strip().lower()
        
        if user_input == 'exit':
            print("👋 Goodbye!")
            break
        elif user_input == 'listen':
            assistant.listen_and_respond()
        else:
            print("Unknown command. Try 'listen' or 'exit'")

if __name__ == "__main__":
    main()
