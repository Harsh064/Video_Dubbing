from deep_translator import GoogleTranslator
import json

with open("segments/segments.json", "r", encoding="utf-8") as f:
    data = json.load(f)

translated = []
for seg in data:
    english = GoogleTranslator(source='hi', target='en').translate(seg['text'])
    translated.append({
        "start": seg["start"],
        "end": seg["end"],
        "speaker": seg["speaker"],
        "text_en": english
    })

with open("segments/translated_segments.json", "w", encoding="utf-8") as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)
