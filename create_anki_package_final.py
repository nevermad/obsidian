#!/usr/bin/env python3
import genanki
import random
import os
import html
import re

# Configuration
input_file = "GO/Часть 1 - Устройство памяти и базовые типы данных/Ответы/ANKI.txt"
output_file = "GO_Part1_Anki_final.apkg"

# Create a unique model ID and deck ID
model_id = random.randrange(1 << 30, 1 << 31)
deck_id = random.randrange(1 << 30, 1 << 31)

# Define the model (card type)
model = genanki.Model(
    model_id,
    'Basic',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

# Create a new deck
deck = genanki.Deck(
    deck_id,
    'GO Part 1 - Memory and Basic Data Types')

# Function to properly escape HTML content
def process_content(content):
    # Replace Go code patterns that cause issues
    # Replace for loops with < with a safe version
    content = re.sub(r'for\s+\w+\s*:?=\s*\d+;\s*\w+\s*<\s*', 'for i := 0; i < ', content)
    content = re.sub(r'<-', '←', content)  # Replace channel operators
    content = re.sub(r'<<', '«', content)  # Replace left shift
    content = re.sub(r'>>', '»', content)  # Replace right shift
    
    # Replace <br> with a placeholder
    content = content.replace('<br>', '___BR___')
    
    # Escape HTML
    content = html.escape(content)
    
    # Restore <br> tags
    content = content.replace('___BR___', '<br>')
    
    # Fix markdown formatting
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)  # Italic
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)  # Code
    
    # Restore special characters
    content = content.replace('←', '&larr;')  # HTML arrow for channel operator
    content = content.replace('«', '&laquo;')  # HTML double angle for left shift
    content = content.replace('»', '&raquo;')  # HTML double angle for right shift
    
    return content

# Read the tab-separated file and add notes to the deck
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Split the line into question and answer
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            question = parts[0]
            answer = parts[1]
            
            # Process content to handle HTML properly
            question = process_content(question)
            answer = process_content(answer)
            
            # Create a note and add it to the deck
            note = genanki.Note(
                model=model,
                fields=[question, answer]
            )
            deck.add_note(note)

# Create a package
package = genanki.Package(deck)

# Save the package
package.write_to_file(output_file)

print(f"Anki package created: {output_file}")
print(f"Total cards: {len(deck.notes)}")
