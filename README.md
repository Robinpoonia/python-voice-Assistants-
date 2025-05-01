# 🎙️ Voice Assistant (React + Django)

This is a local voice assistant web app that records audio via your microphone, sends it to a Django backend for transcription, and responds using a language model.

---

## 🚀 Run Locally

### 📦 Prerequisites

- Python 3.8+
- Node.js + npm
- Git
- FFmpeg (for audio handling)
- Virtualenv (recommended)

---

## 🖥 Backend Setup (Django)

```bash
# Clone the project
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant/backend

# Set up virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver
🔥 API Endpoint
Your Django backend should expose:

http
Copy
Edit
POST http://localhost:8000/api/transcribe-audio/
Request: Multipart form with audio file (audio/mpeg)
Response:

json
Copy
Edit
{
  "transcript": "What the user said",
  "llm_response": "Assistant's response"
}
🌐 Frontend Setup (React)
bash
Copy
Edit
cd ../frontend

# Install frontend dependencies
npm install

# Start development server
npm start
Then open your browser and go to:

arduino
Copy
Edit
http://localhost:3000
📁 File Structure Overview
bash
Copy
Edit
voice-assistant/
├── backend/
│   ├── views.py          # Handle audio and LLM
│   ├── urls.py
│   ├── settings.py
├── frontend/
│   ├── src/
│   │   └── components/
│   │       └── VoiceInputButton.jsx
│   └── App.jsx
├── README.md
✅ Working Flow
🎤 Click Record

📡 Sends audio to Django /api/transcribe-audio/

🧠 Backend transcribes and generates LLM response

🔊 Frontend speaks the response aloud

❗ Troubleshooting
Make sure CORS is enabled in Django for localhost:3000

Install ffmpeg if you face audio decoding issues

Run npm start and python manage.py runserver in separate terminals

