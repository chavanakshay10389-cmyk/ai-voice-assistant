# 🎤 AI Voice Assistant

An intelligent voice assistant application powered by OpenAI's GPT and Google Cloud's speech recognition and text-to-speech services.

## Features

- 🎙️ **Speech Recognition** - Convert voice input to text using Google Speech-to-Text
- 🤖 **AI Responses** - Get intelligent responses from OpenAI's GPT model
- 🔊 **Text-to-Speech** - Convert AI responses back to natural-sounding speech
- 💬 **Conversation Memory** - Maintains conversation history for context-aware responses
- 🌐 **REST API** - Flask-based web API for easy integration
- 🖥️ **CLI Interface** - Command-line interface for direct interaction

## Prerequisites

- Python 3.8+
- Google Cloud Account with Speech-to-Text and Text-to-Speech APIs enabled
- OpenAI API key
- Microphone (for voice input)
- Speaker (for audio output)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/chavanakshay10389-cmyk/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to Google Cloud credentials JSON file

5. **Set up Google Cloud credentials**
   - Download service account credentials from Google Cloud Console
   - Set the path in `.env`

## Usage

### CLI Mode

```bash
python main.py
```

Commands:
- `listen` - Start listening for voice input
- `exit` - Quit the application

### Web API Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

**Health Check**
```bash
GET /health
```

**Transcribe Audio**
```bash
POST /transcribe
Content-Type: multipart/form-data

audio: <audio_file>
```

**Chat with AI**
```bash
POST /chat
Content-Type: application/json

{"message": "Hello, how are you?"}
```

**Synthesize Speech**
```bash
POST /synthesize
Content-Type: application/json

{"text": "Hello, I am doing great!"}
```

**Full Voice Interaction**
```bash
POST /voice-interact
Content-Type: multipart/form-data

audio: <audio_file>
```

**Reset Conversation**
```bash
POST /reset-conversation
```

## Project Structure

```
ai-voice-assistant/
├── main.py                 # CLI entry point
├── app.py                  # Flask web API
├── voice_assistant.py      # Core voice assistant logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Cloud credentials |
| `FLASK_ENV` | Flask environment (development/production) |
| `FLASK_DEBUG` | Enable debug mode (0/1) |

## Requirements

See `requirements.txt` for all dependencies:
- openai - OpenAI API client
- python-dotenv - Environment variable management
- google-cloud-speech - Google Speech-to-Text
- google-cloud-texttospeech - Google Text-to-Speech
- flask - Web framework
- pyaudio - Audio recording/playback
- librosa - Audio processing

## Architecture

```
User Input (Voice)
       ↓
   Record Audio
       ↓
Google Speech-to-Text
       ↓
Transcribed Text
       ↓
OpenAI GPT Model
       ↓
AI Response
       ↓
Google Text-to-Speech
       ↓
Audio Output (Speech)
```

## Error Handling

The application includes comprehensive error handling for:
- Audio recording failures
- Transcription errors
- API connectivity issues
- Invalid input formats

## Performance Considerations

- Audio recording: 16kHz sample rate for optimal performance
- Model: GPT-3.5-turbo for fast responses
- Temperature: 0.7 for balanced creativity and coherence

## Future Enhancements

- [ ] Support for multiple languages
- [ ] User authentication and profiles
- [ ] Conversation history persistence
- [ ] Advanced NLP features
- [ ] Integration with external APIs
- [ ] Web UI with React/Vue
- [ ] Docker containerization
- [ ] Database integration

## Troubleshooting

### Microphone not found
- Check audio device connections
- Update PyAudio: `pip install --upgrade pyaudio`

### Google Cloud API errors
- Verify credentials JSON path
- Check API is enabled in Google Cloud Console

### OpenAI API errors
- Verify API key is correct
- Check account has sufficient credits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue.

---

**Note:** This is a demonstration project. For production use, implement proper security measures, rate limiting, and error handling.
