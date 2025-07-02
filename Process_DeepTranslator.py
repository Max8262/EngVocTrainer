import pickle
import os
from gtts import gTTS
import random
import time
from deep_translator import GoogleTranslator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from pydub import AudioSegment
import tempfile

# Your existing variables
Easy = ["One", "Two"]
Medium = ["Three", "Four"]  
Hard = ["Five", "Six"]

medium_var = 0.5
hard_var = 0.4
desired_len = 37


def load_cached_words():
    try:
        with open('cached_words.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

def save_cached_words(easy, medium, hard):
    with open('cached_words.pkl', 'wb') as f: # Save vocs to pkl
        pickle.dump({
            'easy': easy,
            'medium': medium,
            'hard': hard
        }, f)
    print("SAVED !")


# Try to load from cache first
cached = load_cached_words()

if cached:
    Easy_Word_List = cached['easy']
    Medium_Word_List = cached['medium']
    Hard_Word_List = cached['hard']
    print(f"Loaded from cache: {len(Easy_Word_List)} easy, {len(Medium_Word_List)} medium, {len(Hard_Word_List)} hard words")
else:
    # Initialize deep-translator
    translator = GoogleTranslator(source='en', target='zh-TW') #zh-TW is specs
    
    Easy_Word_List = []
    Medium_Word_List = []
    Hard_Word_List = []
    
    print("Loading Easy Words ......")
    for i in Easy:
        print(f"Processing Level{i}.txt...")
        with open(f"Level{i}.txt", "r", encoding="utf-8") as file: # utf-8 for preventing chinese characters
            for line_num, line in enumerate(file, 1):
                try:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split() # Split by space and take first two parts
                    if len(parts) >= 2:
                        vocab = parts[0]
                        vocab_type = parts[1]
                        
                        print(f"translating: {vocab}")
                        zhtw = translator.translate(vocab)
                        Easy_Word_List.append((vocab, vocab_type, zhtw))
                        time.sleep(0.1)  # prevents translation module from breaking
                    
                except Exception as e:
                    print(f"Error on line {line_num}: {e}")
                    continue
    
    print("Loading Medium Words ......")
    for i in Medium:
        print(f"Processing Level{i}.txt...")
        with open(f"Level{i}.txt", "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                try:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 2:
                        vocab = parts[0]
                        vocab_type = parts[1]
                        
                        print(f"Translating: {vocab}")
                        zhtw = translator.translate(vocab)
                        Medium_Word_List.append((vocab, vocab_type, zhtw))
                        time.sleep(0.1)
                        
                except Exception as e:
                    print(f"Error on line {line_num}: {e}")
                    continue
    
    print("Loading Hard Words ......")
    for i in Hard:
        print(f"Processing Level{i}.txt...")
        with open(f"Level{i}.txt", "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                try:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 2:
                        vocab = parts[0]
                        vocab_type = parts[1]
                        
                        print(f"Translating: {vocab}")
                        zhtw = translator.translate(vocab)
                        Hard_Word_List.append((vocab, vocab_type, zhtw))
                        time.sleep(0.1)
                        
                except Exception as e:
                    print(f"Error on line {line_num}: {e}")
                    continue
    
    # Save to cache
    save_cached_words(Easy_Word_List, Medium_Word_List, Hard_Word_List)

print(f"Final counts: Easy={len(Easy_Word_List)}, Medium={len(Medium_Word_List)}, Hard={len(Hard_Word_List)}")

# Now your random sampling with safety checks



medium_needed = int(desired_len * medium_var)
hard_needed = int(desired_len * hard_var)
easy_needed = desired_len - medium_needed - hard_needed


if len(Easy_Word_List) < easy_needed:
    Rand_Easy = Easy_Word_List
else:
    Rand_Easy = random.sample(Easy_Word_List, easy_needed)

if len(Medium_Word_List) < medium_needed:
    Rand_Medium = Medium_Word_List
else:
    Rand_Medium = random.sample(Medium_Word_List, medium_needed)

if len(Hard_Word_List) < hard_needed:
    Rand_Hard = Hard_Word_List
else:
    Rand_Hard = random.sample(Hard_Word_List, hard_needed)

Final_Question = Rand_Easy + Rand_Medium + Rand_Hard
random.shuffle(Final_Question)

print(f"Selected {len(Final_Question)} words for quiz")

date = time.time()
date = time.ctime(date)
def create_vocab_form(word_list, filename="vocab_form.pdf", boxes = desired_len):
    # Create PDF canvas
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    # Title
    c.setFont("Times-Roman", 24)
    c.drawCentredString(width/2, height - 40, "Vocabulary Quiz Form")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width - 80, height - 60, f"Date : {date}")
    
    # Calculate box dimensions
    cols = 5
    rows = 0

    if boxes % 5 == 0 :
        rows = boxes // 5 
    else:
        rows = (boxes // 5) + 1

    margin = 50
    box_width = (width - 2*margin) / cols
    box_height = 40
    # Starting position
    start_x = margin
    start_y = height - 85
    
    # Draw grid of boxes
    for row in range(rows):
        for col in range(cols):
            # Calculate position
            x = start_x + col * box_width
            y = start_y - row * box_height
            # Draw box border
            c.rect(x, y - box_height, box_width, box_height)
            # Add question number
            question_num = row * cols + col + 1
            if question_num <= boxes: 
                c.setFont("Helvetica", 10)
                c.drawString(x + 5, y - 10, f"Q{question_num}")
            else:
                c.line(x + box_width, y, x, y - box_height)
    # Save PDF
    c.save()

    print(f"PDF saved as {filename}")



def create_answer_key(word_list, filename="vocab_answer_key.pdf", boxes = desired_len):
    # Create PDF canvas
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    # Title
    c.setFont("Times-Roman", 24)
    c.drawCentredString(width/2, height - 40, "Vocabulary Quiz Form -- Answer Key")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width - 80, height - 60, f"Date : {date}")
    
    # Calculate box dimensions
    cols = 5
    rows = 0

    if boxes % 5 == 0 :
        rows = boxes // 5 
    else:
        rows = (boxes // 5) + 1

    margin = 50
    box_width = (width - 2*margin) / cols
    box_height = 40
    # Starting position
    start_x = margin
    start_y = height - 85
    
    # Draw grid of boxes
    for row in range(rows):
        for col in range(cols):
            # Calculate position
            x = start_x + col * box_width
            y = start_y - row * box_height
            # Draw box border
            c.rect(x, y - box_height, box_width, box_height)
            # Add question number
            question_num = row * cols + col + 1

            if question_num <= boxes: 
                c.setFont("Helvetica", 10)
                c.drawString(x + 5, y - 10, f"Q{question_num}")
                word_data = word_list[question_num - 1]
                english = word_data[0] if isinstance(word_data, tuple) else word_data
                
                # CENTER THE TEXT PROPERLY
                c.setFont("Helvetica-Bold", 12)
                text_width = c.stringWidth(english, "Helvetica-Bold", 12)
                center_x = x + (box_width - text_width) / 2
                center_y = y - 25  # Vertically center in box
                c.drawString(center_x, center_y, english)
            else:
                c.line(x + box_width, y, x, y - box_height)
            
    # Save PDF
    c.save()
    print(f"PDF saved as {filename}")

def AudioCreation(word_list, desired_len, output_file="quiz_audio.mp3"):
    combined = AudioSegment.empty()
    silence = AudioSegment.silent(duration=1300)
    
    for i, word_data in enumerate(word_list):
        english_word = word_data[0]
        question_numero = f"Numero_Audio/Question{i+1}.mp3"  # Fixed: i+1 for proper numbering
        
        # Check if question audio exists
        if os.path.exists(question_numero):
            question_audio = AudioSegment.from_mp3(question_numero)
        else:
            print(f"Warning: {question_numero} not found, skipping question number")
            question_audio = AudioSegment.empty()  # Use empty audio if file missing
        
        word_file = f"Stored_Audio/{english_word}.mp3"
        if os.path.exists(word_file):
            word_audio = AudioSegment.from_mp3(word_file)
            combined += question_audio + silence + word_audio + silence
        else:
            print(f"Warning: {word_file} not found, skipping word")
    
    
    combined.export(output_file, format="mp3")
    print(f"Quiz audio saved as {output_file}")


def main():
    create_vocab_form(Final_Question)  
    create_answer_key(Final_Question)
    AudioCreation(Final_Question, desired_len)


if __name__ == "__main__":
    main()
