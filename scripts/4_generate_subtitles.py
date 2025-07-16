import json

with open("segments/translated_segments.json", "r", encoding="utf-8") as f:
    segments = json.load(f)

def seconds_to_srt_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

with open("output/subtitles.srt", "w", encoding="utf-8") as f:
    for idx, seg in enumerate(segments, start=1):
        f.write(f"{idx}\n")
        f.write(f"{seconds_to_srt_time(seg['start'])} --> {seconds_to_srt_time(seg['end'])}\n")
        f.write(f"{seg['text_en']}\n\n")
