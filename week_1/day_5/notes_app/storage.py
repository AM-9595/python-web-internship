import json
import os
from datetime import datetime

FILE_NAME = "notes.json"

def load_notes():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        notes = json.load(f)
    return notes

def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def add_note(text):
    notes = load_notes()
    if notes:
        new_id = max(n["id"] for n in notes) + 1
    else:
        new_id = 1
    today = datetime.now().strftime("%Y-%m-%d")
    new_note = {
        "id": new_id,
        "text": text,
        "created_at": today
    }
    notes.append(new_note)
    save_notes(notes)

def delete_note(note_id):
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[i]
            save_notes(notes)
            return True
    return False

def search_notes(keyword):
    notes = load_notes()
    result = []
    keyword_lower = keyword.lower()
    for note in notes:
        if keyword_lower in note["text"].lower():
            result.append(note)
    return result