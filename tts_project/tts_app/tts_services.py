import asyncio
import edge_tts
from gtts import gTTS
import requests

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
        "r": "0",
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