import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_IDS = {
    "SPEAKER_00": "IKne3meq5aSn9XLyUdCD",
    "SPEAKER_01": "N2lVS1w4EtoT3dr4eOWO"
}

with open("segments/translated_segments.json", "r", encoding="utf-8") as f:
    data = json.load(f)

os.makedirs("segments", exist_ok=True)

def generate_voice(text, speaker_id, idx):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_IDS[speaker_id]}/stream"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    out_path = f"segments/segment_{idx}.mp3"
    with open(out_path, "wb") as f:
        f.write(response.content)
    return out_path

audio_segments = []
for idx, seg in enumerate(data):
    path = generate_voice(seg["text_en"], seg["speaker"], idx)
    audio_segments.append((seg["start"], path))

# Save final audio segment list for merging
with open("segments/audio_segment_list.json", "w") as f:
    json.dump(audio_segments, f)

# import os
# import requests
# import json
# from dotenv import load_dotenv
# from pydub import AudioSegment
# from pydub.utils import mediainfo
# import time

# load_dotenv()
# ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
# VOICE_IDS = {
#     "SPEAKER_00": "IKne3meq5aSn9XLyUdCD",
#     "SPEAKER_01": "N2lVS1w4EtoT3dr4eOWO"
# }

# # Create output directory
# os.makedirs("segments", exist_ok=True)

# def validate_audio_file(file_path):
#     """Check if audio file is valid and properly formatted"""
#     try:
#         audio = AudioSegment.from_file(file_path)
#         if len(audio) == 0:
#             return False
#         info = mediainfo(file_path)
#         return info["format_name"].lower() == "mp3"
#     except Exception:
#         return False

# def generate_voice(text, speaker_id, idx, max_retries=3):
#     """Generate voice with retries and validation"""
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_IDS[speaker_id]}"
#     headers = {
#         "xi-api-key": ELEVEN_API_KEY,
#         "Content-Type": "application/json",
#         "Accept": "audio/mpeg"  # Ensure we get proper MP3 format
#     }
#     payload = {
#         "text": text,
#         "model_id": "eleven_monolingual_v2",  # Use specific model
#         "voice_settings": {
#             "stability": 0.75,
#             "similarity_boost": 0.75,
#             "style": 0.5,
#             "speaker_boost": True
#         }
#     }
    
#     out_path = f"segments/segment_{idx}.mp3"
#     temp_path = f"segments/temp_{idx}.mp3"
    
#     for attempt in range(max_retries):
#         try:
#             # Make the API request with timeout
#             response = requests.post(
#                 url, 
#                 headers=headers, 
#                 json=payload,
#                 timeout=30
#             )
#             response.raise_for_status()
            
#             # Save to temporary file first
#             with open(temp_path, "wb") as f:
#                 f.write(response.content)
            
#             # Validate the audio file
#             if validate_audio_file(temp_path):
#                 os.replace(temp_path, out_path)
#                 print(f"✅ Successfully generated segment {idx}")
#                 return out_path
#             else:
#                 print(f"⚠️ Retrying segment {idx} - invalid audio format")
                
#         except requests.exceptions.RequestException as e:
#             print(f"⚠️ Attempt {attempt + 1} failed for segment {idx}: {str(e)}")
        
#         time.sleep(1)  # Brief delay between retries
    
#     print(f"❌ Failed to generate valid audio for segment {idx} after {max_retries} attempts")
#     return None

# def main():
#     # Load translated segments
#     with open("segments/translated_segments.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
    
#     audio_segments = []
#     failed_segments = []
    
#     for idx, seg in enumerate(data):
#         path = generate_voice(seg["text_en"], seg["speaker"], idx)
#         if path:
#             audio_segments.append((seg["start"], path))
#         else:
#             failed_segments.append(idx)
    
#     # Save successful audio segments
#     with open("segments/audio_segment_list.json", "w") as f:
#         json.dump(audio_segments, f)
    
#     # Report any failures
#     if failed_segments:
#         print(f"\n❌ Failed to generate segments: {failed_segments}")
#         print("Possible solutions:")
#         print("1. Check your ElevenLabs API key and quota")
#         print("2. Verify the voice IDs are correct")
#         print("3. Try shorter text segments")
#     else:
#         print("\n🎉 All audio segments generated successfully!")

# if __name__ == "__main__":
#     main()