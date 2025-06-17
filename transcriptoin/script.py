from email.mime import text
import whisper
import os
from datetime import datetime
os.environ["PATH"] += os.pathsep + r"C:\Users\pardh\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

save_path = r"D:\coding\intel\ai classroom assistant\transcription\transcripts"
os.makedirs(save_path, exist_ok=True)
timedate = datetime.now().strftime("%Y-%m-%d_%H-%M")
outpath = os.path.join(save_path, f"text_{timedate}.txt")
audiopath = r"D:\coding\intel\ai classroom assistant\transcription\recordings\rec_2025.06.16.08.56.wav"
wmodel = whisper.load_model("small")


transtext = wmodel.transcribe(audiopath, language="en")


with open(outpath, "w",) as f:
    f.write(transtext["text"])
# print(transcription)
print(f"Saved as '{outpath}.txt' file")
