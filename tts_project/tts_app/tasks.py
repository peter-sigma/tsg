import asyncio
import logging
from .tts_services import tts_using_edge, tts_using_gtts, tts_using_voicerss

logger = logging.getLogger(__name__)

def process_tts_task(text, voice_choice, output_path):
    logger.info("Starting TTS conversion for voice_choice: %s, output_path: %s", voice_choice, output_path)
    try:
        if voice_choice == 'edge_female':
            voice = "en-US-JennyNeural"
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(tts_using_edge(text, voice, output_path))
            loop.close()
        elif voice_choice == 'edge_male':
            voice = "en-US-GuyNeural"
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(tts_using_edge(text, voice, output_path))
            loop.close()
        elif voice_choice == 'gtts':
            tts_using_gtts(text, language="en", output_file=output_path)
        elif voice_choice.startswith('voicerss_'):
            voice = voice_choice.split('_')[1].capitalize()
            tts_using_voicerss(text, language="en-us", voice=voice, output_file=output_path)
        logger.info("TTS conversion completed; file should be saved at: %s", output_path)
    except Exception as e:
        logger.exception("Error during TTS conversion: %s", e)
