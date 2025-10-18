# Transcribe AI

A high-performance FastAPI-based audio transcription service that converts audio files to text using advanced AI transcription technology. This service provides a RESTful API for asynchronous audio transcription with support for multiple languages and accuracy levels.

## Features

- 🎵 **Audio Transcription**: Convert audio files to text using AI-powered transcription
- 🌍 **Multi-language Support**: Support for 15+ languages including English, French, German, Spanish, Arabic, and more
- ⚡ **Asynchronous Processing**: Non-blocking transcription requests with event-based status checking
- 🎯 **Multiple Accuracy Levels**: Choose between low, medium, and high accuracy settings
- 👥 **Speaker Diarization**: Optional speaker identification and separation
- 🚀 **FastAPI Framework**: Modern, fast, and auto-documented REST API
- 📊 **Real-time Status**: Check transcription progress with event IDs

## Supported Languages

- English (en)
- French (fr)
- German (de)
- Spanish (es)
- Italian (it)
- Portuguese (pt)
- Dutch (nl)
- Polish (pl)
- Russian (ru)
- Turkish (tr)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Persian/Farsi (fa)
- and many more...
## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/RayanErfan/transcribe-ai.git
cd transcribe-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python src/main.py
```

The API will be available at `http://localhost:54004`

### API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:54004/docs`
- ReDoc: `http://localhost:54004/redoc`

### API Endpoints

#### 1. Start Transcription

**POST** `/transcribe`

Start a new transcription job.

**Request Body:**
```json
{
  "path": "https://example.com/audio.mp3",
  "type": 1,
  "lang_code": "en",
  "diarization": false,
  "accuracy": "medium"
}
```

**Response:**
```json
{
  "status": "ok",
  "event_id": "unique_event_id_here"
}
```

#### 2. Check Transcription Status

**POST** `/check_event`

Check the status of a transcription job.

**Request Body:**
```json
{
  "event_id": "unique_event_id_here"
}
```

**Response (Pending):**
```json
{
  "status": "pending",
  "message": "failed, please retry"
}
```

**Response (Completed):**
```json
{
  "status": "ok",
  "audio_url": "https://example.com/audio.mp3",
  "transcript": "Transcribed text content here..."
}
```

### Example Usage

```python
import requests

# Start transcription
response = requests.post("http://localhost:54004/transcribe", json={
    "path": "https://example.com/audio.mp3",
    "lang_code": "en",
    "accuracy": "high"
})

event_id = response.json()["event_id"]

# Check status
status_response = requests.post("http://localhost:54004/check_event", json={
    "event_id": event_id
})

if status_response.json()["status"] == "ok":
    transcript = status_response.json()["transcript"]
    print(f"Transcription: {transcript}")
```

## Configuration

The service can be configured by modifying `src/config.py`:

```python
class Config:
    START_URL = "https://notegpt.io/api/v2/transcriptions/start"
    CHECK_URL = "https://notegpt.io/api/v2/transcriptions"
    API_HOST = "0.0.0.0"
    API_PORT = 54004
```

## Development

### Project Structure

```
transcribe-ai/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── config.py        # Configuration settings
│   └── utils.py         # Utility functions (hashing, etc.)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # MIT License
```

### Dependencies

- **FastAPI**: Modern web framework for building APIs
- **aiohttp**: Asynchronous HTTP client/server
- **uvicorn**: ASGI server for running FastAPI applications
- **pydantic**: Data validation using Python type annotations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Rayan Erfan**
- GitHub: [@RayanErfan](https://github.com/RayanErfan)

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by advanced AI transcription technology
- Inspired by the need for accessible audio-to-text conversion

---

⭐ If you found this project helpful, please give it a star on GitHub!