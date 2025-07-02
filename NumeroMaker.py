#Importing Stuff
import edge_tts
import os
from num2words import num2words

Numero_Audio = "Numero_Audio"

if not os.path.exists(Numero_Audio):
    os.makedirs(Numero_Audio)

def TTS():
    for i in range(100):
        try:
            Numero = f"Question{i+1}"
            filename = f"{Numero}.mp3"
            filepath = os.path.join(Numero_Audio, filename)
            communicate = edge_tts.Communicate(Numero, "en-US-AriaNeural")
            communicate.save_sync(filepath)
            print(f"Created: {filename}")
        except Exception as e:
            print(f"Error: {e}")

# Run the function normally
TTS()