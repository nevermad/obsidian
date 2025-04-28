#!/usr/bin/env python3
import genanki
import random
import os
import html
import re

# Configuration
input_directory = "/Users/fapus/Obsidian/fapus/GO/Часть 3 - Go Runtime/Ответы"
anki_txt_file = os.path.join(input_directory, "ANKI.txt")
output_file = os.path.join(input_directory, "GO_Part3_Anki.apkg")

# Create a unique model ID and deck ID
model_id = random.randrange(1 << 30, 1 << 31)
deck_id = random.randrange(1 << 30, 1 << 31)

# Define the model (card type) with custom CSS for code blocks
model = genanki.Model(
    model_id,
    'Basic with Code Formatting',
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
    ],
    css='''
    .card {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 16px;
        text-align: left;
        color: black;
        background-color: white;
        line-height: 1.5em;
    }
    code {
        font-family: Menlo, Monaco, 'Courier New', monospace;
        background-color: #f5f5f5;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 90%;
        color: #c7254e;
    }
    pre {
        margin: 10px 0;
        padding: 12px;
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 4px;
        overflow-x: auto;
    }
    pre code {
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        font-size: 14px;
        color: #333;
        line-height: 1.4;
        display: block;
        white-space: pre;
    }
    b {
        font-weight: bold;
        color: #333;
    }
    i {
        font-style: italic;
    }
    ''')

# Create a new deck
deck = genanki.Deck(
    deck_id,
    'GO Part 3 - Go Runtime')

# Function to properly escape HTML content and improve code formatting
def process_content(content):
    # Replace Go code patterns that cause issues
    content = re.sub(r'for\s+\w+\s*:?=\s*\d+;\s*\w+\s*<\s*', 'for i := 0; i < ', content)
    content = re.sub(r'<-', '←', content)  # Replace channel operators
    content = re.sub(r'<<', '«', content)  # Replace left shift
    content = re.sub(r'>>', '»', content)  # Replace right shift
    
    # Replace <br> with a placeholder
    content = content.replace('<br>', '___BR___')
    
    # Process HTML code block first before general HTML escaping
    def code_block_replace(match):
        code_content = match.group(1)
        # Ensure line breaks are preserved and indentation is maintained
        code_content = code_content.replace('\n', '___NEWLINE___')
        return '___CODE_BLOCK___' + code_content + '___END_CODE_BLOCK___'
    
    # Handle both <pre><code> and regular code blocks
    content = re.sub(r'<pre><code>(.*?)</code></pre>', code_block_replace, content, flags=re.DOTALL)
    
    # Escape HTML
    content = html.escape(content)
    
    # Restore code blocks with proper formatting
    def restore_code_block(match):
        code_content = match.group(1)
        # Restore linebreaks and indent properly
        code_content = code_content.replace('___NEWLINE___', '\n')
        return f'<pre><code>{code_content}</code></pre>'
    
    content = re.sub(r'___CODE_BLOCK___(.*?)___END_CODE_BLOCK___', restore_code_block, content, flags=re.DOTALL)
    
    # Restore <br> tags
    content = content.replace('___BR___', '<br>')
    
    # Fix markdown formatting
    content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)  # Italic
    content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)  # Inline code
    
    # Restore special characters
    content = content.replace('←', '&larr;')  # HTML arrow for channel operator
    content = content.replace('«', '&laquo;')  # HTML double angle for left shift
    content = content.replace('»', '&raquo;')  # HTML double angle for right shift
    
    return content

# Function to extract questions and answers from markdown file
def extract_qa_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get the file title without '.md' extension
    file_title = os.path.basename(file_path)
    if file_title.endswith('.md'):
        file_title = file_title[:-3]  # Remove .md extension
    
    # Новое регулярное выражение: вопрос — любая строка, начинающаяся с '## ', ответ — до следующего '## ' или конца файла
    questions_pattern = r'## ?(.*?)\n(.*?)(?=\n## |\Z)'
    qa_pairs = re.findall(questions_pattern, content, re.DOTALL)
    
    qa_results = []
    for question, answer in qa_pairs:
        answer = answer.strip()
        
        # Обработка code block
        answer = re.sub(r'```go\s*\n(.*?)\n```', r'<pre><code>\1</code></pre>', answer, flags=re.DOTALL)
        answer = re.sub(r'```(?:\w*)\s*\n(.*?)\n```', r'<pre><code>\1</code></pre>', answer, flags=re.DOTALL)
        
        # Add file title context to the question
        full_question = f"{file_title}: {question.strip()}"
        qa_results.append((full_question, answer))
    
    return qa_results

# Process all markdown files in the directory
questions_answers = []
with open(anki_txt_file, 'w', encoding='utf-8') as anki_txt:
    # Sort files for consistent order
    md_files = [f for f in os.listdir(input_directory) if f.endswith('.md')]
    md_files.sort()
    
    for filename in md_files:
        if filename.endswith('.md'):
            file_path = os.path.join(input_directory, filename)
            
            # Skip non-content files
            if filename.lower() == 'anki.md' or filename.startswith('create_anki'):
                continue
                
            print(f"Processing {filename}...")
            qa_pairs = extract_qa_from_markdown(file_path)
            
            for question, answer in qa_pairs:
                # Write to ANKI.txt
                anki_txt.write(f"{question}\t{answer}\n")
                
                # Add to the list for the Anki deck
                questions_answers.append((question, answer))

# Add notes to the deck
for question, answer in questions_answers:
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

print(f"ANKI text file created: {anki_txt_file}")
print(f"Anki package created: {output_file}")
print(f"Total cards: {len(deck.notes)}") 