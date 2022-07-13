
import random
from gtts import *
import playsound    # to play mp3 file
import os           # to remove audio file
from os.path import exists


def say(text: str, block = True, lang = 'en'):
    """Text-to-speech synthesis using google TTS. If block=True,
        waits until the text is spoken. If False, return a cleanup
        function to delete the temporary audio file."""
    audio_file = f'audio-{random.randint(0, 1000000)}.mp3'
    try:
        gTTS(text, lang = lang).save(audio_file)
        playsound.playsound(audio_file, block = block)
    except gTTSError:
        print('unknown error')

    if block:
        os.remove(audio_file)
    else:
        print(f"Playing sound, don't forget to do: os.remove('{audio_file}')"
              "\n(You can do so by calling the returned function.)")
        return(lambda: os.remove(audio_file))

    if exists(audio_file):
        os.remove(audio_file)
