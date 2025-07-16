from moviepy import VideoFileClip, AudioFileClip, concatenate_audioclips
from pydub import AudioSegment

import json

# Load audio segments
with open("segments/audio_segment_list.json", "r") as f:
    segment_list = json.load(f)

final_audio = AudioSegment.silent(duration=VideoFileClip("input/input_video.mp4").duration * 1000)

for start_time, path in segment_list:
    segment = AudioSegment.from_file(path)
    final_audio = final_audio.overlay(segment, position=int(start_time * 1000))

final_audio.export("output/translated_audio.mp3", format="mp3")

# Replace audio and add subtitles
video = VideoFileClip("input/input_video.mp4")
audio = AudioFileClip("output/translated_audio.mp3")
final_video = video.with_audio(audio)
final_video.write_videofile("output/english_dubbed_video.mp4", codec="libx264", audio_codec="aac")
