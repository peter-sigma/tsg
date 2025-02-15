import os
import asyncio
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import TTSForm

# For gTTS
from gtts import gTTS

# For edge-tts
import edge_tts
import requests

# A simple folder to store generated audio files
AUDIO_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# Function to run Edge TTS conversion (async)
async def tts_using_edge(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def tts_using_gtts(text, language="en", output_file="gtts.mp3"):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)



def tts_using_voicerss(text, language="en-us", voice="Linda", output_file="voicerss.mp3"):
    API_KEY = "7bdce4f30b76419a9a22ea401af9778f"
    url = "https://api.voicerss.org/"
    params = {
        "key": API_KEY,
        "src": text,
        "hl": language,
        "v": voice,
        "r": "0",               # Adjust speech rate if needed
        "c": "MP3",
        "f": "44khz_16bit_stereo"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {output_file} (VoiceRSS)")
    else:
        print("VoiceRSS Error:", response.status_code, response.text)



def index(request):
    if request.method == 'POST':
        form = TTSForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            voice_choice = form.cleaned_data['voice']

            if voice_choice == 'edge_female':
                voice = "en-US-JennyNeural"
                output_filename = "edge_female.mp3"
                output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
                asyncio.run(tts_using_edge(text, voice, output_path))
            elif voice_choice == 'edge_male':
                voice = "en-US-GuyNeural"
                output_filename = "edge_male.mp3"
                output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
                asyncio.run(tts_using_edge(text, voice, output_path))
            elif voice_choice == 'gtts':
                output_filename = "gtts.mp3"
                output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
                tts_using_gtts(text, language="en", output_file=output_path)
            elif voice_choice.startswith('voicerss_'):
                # Extract the voice name after the underscore
                voice = voice_choice.split('_')[1].capitalize()  # e.g., "linda" -> "Linda"
                output_filename = f"voicerss_{voice.lower()}.mp3"
                output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
                tts_using_voicerss(text, language="en-us", voice=voice, output_file=output_path)
            else:
                output_filename = None

            if output_filename:
                return HttpResponseRedirect(reverse('tts_app:result') + f'?audio={output_filename}')
    else:
        form = TTSForm()
    return render(request, 'tts_app/index.html', {'form': form})


def result(request):
    audio_file = request.GET.get('audio')
    audio_url = None
    if audio_file:
        # Build URL to the audio file served from the static directory.
        audio_url = f'/static/audio/{audio_file}'
    return render(request, 'tts_app/result.html', {'audio_url': audio_url})