import os
import json
import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline
import whisper
from moviepy import VideoFileClip
from huggingface_hub import login
import json

# ===== WINDOWS-SPECIFIC FIXES =====
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'
os.environ['PYANNOTE_CACHE'] = os.path.abspath("./pyannote_cache")
os.environ['SPEEECHBRAIN_CACHE'] = os.path.abspath("./speechbrain_cache")

# Force SpeechBrain to use copy instead of symlinks
os.environ['SB_DOWNLOAD_STRATEGY'] = 'copy'  # <-- CRITICAL FIX

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

input_path = "input/input_video.mp4"
audio_path = "input/temp.wav"


# # Step 1: Extract audio
# print("🎬 Extracting audio...")
# video = VideoFileClip(input_path)
# video.audio.write_audiofile(audio_path, codec='pcm_s16le')

# # Step 2: Transcribe with local Whisper
# print("🧠 Transcribing using local Whisper...")
# whisper_model = whisper.load_model("medium")
# result = whisper_model.transcribe(audio_path, language="hi")

# # Extract segments
# segments = result["segments"]
###############################
# Save to file
# with open('transcription_result.json', 'w', encoding='utf-8') as f:
#     json.dump({
#         'full_result': result,
#         'segments': segments
#     }, f, ensure_ascii=False, indent=4)

# Later, to load it back:
with open('transcription_result.json', 'r', encoding='utf-8') as f:
    saved_data = json.load(f)
    result = saved_data['full_result']
    segments = saved_data['segments']
    ######################
# Step 3: Speaker Diarization using pyannote
print("🧍‍♂️ Running speaker diarization...")

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=HF_TOKEN,cache_dir="./pyannote_cache")
diarization = pipeline(audio_path)

# Step 4: Align speakers with transcript
print("🔗 Aligning speakers with transcribed segments...")
aligned_segments = []
speaker_iter = diarization.itertracks(yield_label=True)

for segment, (turn, _, speaker) in zip(segments, speaker_iter):
    aligned_segments.append({
        "start": segment["start"],
        "end": segment["end"],
        "speaker": speaker,
        "text": segment["text"]
    })

# Step 5: Save aligned segments
os.makedirs("segments", exist_ok=True)
with open("segments/segments.json", "w", encoding="utf-8") as f:
    json.dump(aligned_segments, f, ensure_ascii=False, indent=2)

print("✅ Done. Saved to segments/segments.json")
