from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import whisper
import tempfile
import os
import traceback
import warnings
import cohere
from django.conf import settings
import pyttsx3
import tempfile
import base64
# co = cohere.Client(settings.COHERE_API_KEY)
co = cohere.Client("uh7zKhJuc6RSLlDlHAqtKnESvDUy9dWjNzP2Fiui")


# Suppress Whisper warnings about FP16 on CPU
warnings.filterwarnings("ignore", category=UserWarning)

# Load Whisper model once globally
model = whisper.load_model("base")
def get_llm_response(transcript):
    response = co.chat(
        message=f"You are a helpful voice assistant. User said: {transcript}"
    )
    return response.text.strip()

def synthesize_text(text):
    engine = pyttsx3.init()
    
    # Optional: configure voice, rate, etc.
    engine.setProperty('rate', 150)  # speaking speed

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_filename = tmp_file.name
    engine.save_to_file(text, tmp_filename)
    engine.runAndWait()

    # Read and encode to base64
    with open(tmp_filename, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    os.remove(tmp_filename)
    return audio_base64

def handle_audio_transcription(audio_file):
    # Determine file extension or use default
    ext = os.path.splitext(audio_file.name)[1] or ".mp3"

    # Save uploaded audio to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name

    try:
        # Transcribe using Whisper
        result = model.transcribe(temp_path)
        return result['text']
    finally:
        # Always clean up temp file
        os.remove(temp_path)


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello from voice assistant backend!"})



@api_view(["POST"])
def transcribe_audio(request):
    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

    try:
        transcript = handle_audio_transcription(audio_file)
        llm_response = get_llm_response(transcript)
        tts_audio_base64 = synthesize_text(llm_response)
    except Exception as e:
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)

    return JsonResponse({
        'transcript': transcript,
        'llm_response': llm_response,
        'tts_audio': tts_audio_base64
    })
