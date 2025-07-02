#Importing Stuff
import edge_tts
import os
from num2words import num2words

Lvl_List = ["One", "Two", "Three", "Four", "Five", "Six"]
Stored_Audio = "Stored_Audio"

if not os.path.exists(Stored_Audio):
    os.makedirs(Stored_Audio)

def TTS():
    for i in Lvl_List:
        with open(f"Level{i}.txt", "r", encoding="utf-8") as file:
            for line in file:
                try:
                    vocab = line.strip().split()[0]
                    filename = f"{vocab}.mp3"
                    filepath = os.path.join(Stored_Audio, filename)
                    
                    # Sets TTS specs
                    communicate = edge_tts.Communicate(vocab, "en-US-AriaNeural")
                    
                    # Save synchronously (blocks until complete)
                    communicate.save_sync(filepath)
                    print(f"Created: {filename}")
                    
                except Exception as e:
                    print(f"Error: {e}")

# Run the function normally
TTS()