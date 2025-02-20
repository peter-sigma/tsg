import os 
import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import TTSForm
from django_q.tasks import async_task  # Import Django Q's async_task
from .tasks import process_tts_task
from django.conf import settings
from django.http import JsonResponse
import hashlib
from .models import ConversionLog


# (Keep your TTS functions defined here or imported from elsewhere if you refactor)
AUDIO_OUTPUT_DIR = os.path.join(settings.BASE_DIR, 'tts_app', 'static', 'audio')
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)


def index(request):
    if request.method == 'POST':
        form = TTSForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            voice_choice = form.cleaned_data['voice']

            # Generate a cache key from the text and voice parameters.
            cache_key = generate_cache_key(text, voice_choice)

            # Determine the output filename using the cache key.
            if voice_choice == 'edge_female':
                output_filename = f"edge_female_{cache_key}.mp3"
            elif voice_choice == 'edge_male':
                output_filename = f"edge_male_{cache_key}.mp3"
            elif voice_choice == 'gtts':
                output_filename = f"gtts_{cache_key}.mp3"
            elif voice_choice.startswith('voicerss_'):
                # Extract the specific voice name (e.g., 'voicerss_mike' -> 'mike')
                voice = voice_choice.split('_')[1].lower()
                output_filename = f"voicerss_{voice}_{cache_key}.mp3"
            else:
                output_filename = None

            if output_filename:
                output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
                log = ConversionLog.objects.create(
                    text=text,
                    voice=voice_choice,
                    status='PENDING'
                )
                # Check if the file already exists in the cache.
                if os.path.exists(output_path):
                    # If it exists, reuse the cached audio file.
                    print("File retrieved. No need to reconvert.")
                    log.status = 'COMPLETED'
                    log.output_filename = output_filename
                    log.save()
                    return HttpResponseRedirect(reverse('tts_app:result') + f'?audio={output_filename}')
                    # Otherwise, enqueue the TTS conversion task.
                async_task(process_tts_task, text, voice_choice, output_path, log.id)
                return HttpResponseRedirect(
                    reverse('tts_app:result') + f'?audio={output_filename}'
                )
    else:
        form = TTSForm()
    return render(request, 'tts_app/index.html', {'form': form})



def check_status(request):
    audio_file = request.GET.get('audio')
    if not audio_file:
        return JsonResponse({'ready': False, 'error': 'No audio file specified'})
    # Build the absolute file path where the audio is stored.
    file_path = os.path.join(settings.BASE_DIR, 'tts_app', 'static', 'audio', audio_file)
    if os.path.exists(file_path):
        return JsonResponse({'ready': True})
    else:
        return JsonResponse({'ready': False})
    
    

def generate_cache_key(text, voice):
    key_string = f"{text}:{voice}"
    return hashlib.sha256(key_string.encode('utf-8')).hexdigest()



def result(request):
    audio_file = request.GET.get('audio')
    audio_url = None
    if audio_file:
        audio_url = f'/static/audio/{audio_file}'
    return render(request, 'tts_app/result.html', {'audio_url': audio_url})