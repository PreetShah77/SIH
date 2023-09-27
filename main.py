import speech_recognition as sr
from googletrans import Translator
from deep_translator import GoogleTranslator
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS

output_video_path='output_video.mp4'
video_path = 'input.mp4'

video = VideoFileClip(video_path)

audio = video.audio

audio.write_audiofile('output_audio.wav')

video = video.set_audio(None)

# Save the video without audio
video.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)



video.close()
audio.close()

translator = Translator()

recognizer = sr.Recognizer() 
audio_file = "output_audio.wav"  # Replace with your audio file path
with sr.AudioFile(audio_file) as source:
    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise if necessary
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_sphinx(audio_data)
        print("Converted Text (using Pocketsphinx): " + text)
    except sr.UnknownValueError:
        print("Pocketsphinx could not understand the audio")
    except sr.RequestError as e:
        print(f"Speech recognition request failed; {e}")



translated = GoogleTranslator(source='auto', target='hi').translate(text)
print(translated)

myobj = gTTS(text=translated, lang='hi' , slow=False)

myobj.save("translated_audio.mp3")

input_video_path = "output_video.mp4"
translated_audio_path = "translated_audio.mp3"
output_video_path = "final_video.mp4"
video_clip = VideoFileClip(input_video_path)
audio_clip = AudioFileClip(translated_audio_path)
video_clip = video_clip.set_audio(audio_clip)
video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)
print("Translated audio appended to the video.")


import shutil

# Paths to your input video, translated audio, and output video
input_video_path = "input.mp4"
translated_audio_path = "translated_audio.mp3"
output_video_path = "final_video.mp4"

# Load the input video and translated audio
video_clip = VideoFileClip(input_video_path)
audio_clip = AudioFileClip(translated_audio_path)

# Ensure audio duration matches video duration
if audio_clip.duration > video_clip.duration:
    # Trim the audio if it's longer than the video
    audio_clip = audio_clip.subclip(0, video_clip.duration)
elif audio_clip.duration < video_clip.duration:
    # Extend the audio by looping if it's shorter than the video
    num_loops = int(video_clip.duration / audio_clip.duration)
    audio_clip = audio_clip.volumex(num_loops)

# Set the audio of the video to the translated audio
video_clip = video_clip.set_audio(audio_clip)

# Write the final video
video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', threads=4)

# Clean up intermediate files (optional)
shutil.copy(translated_audio_path, "translated_audio_original.mp3")
shutil.move("translated_audio_original.mp3", translated_audio_path)

print("Translated audio appended to the video.")