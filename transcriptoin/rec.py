from pvrecorder import PvRecorder
import soundfile as sf
import numpy as np
import threading
import os
from datetime import datetime

savepath = r"D:\coding\intel\ai classroom assistant\transcription\recordings"
os.makedirs(savepath, exist_ok=True)
timedate = datetime.now().strftime("%Y.%m.%d.%H.%M")
name = os.path.join(savepath, f"rec_{timedate}.wav")
samplingrate = 16000
frame_window = 512
frames = []

interrupt = threading.Event()

def wait():
    input("Recording in progress..\n press ENTER TO STOP")
    interrupt.set()

try:
    mics=PvRecorder.get_available_devices()
    print("Available devices are:")
    for i,mic in enumerate(mics):
        print(f"{i}: {mic}")
    smic=int(input("Select input device:"))
    record = PvRecorder(device_index=smic, frame_length=frame_window)
    record.start()

    f=threading.Thread(target=wait)
    f.start()
    while not interrupt.is_set():
        frame = record.read()
        frames.append(np.array(frame, dtype=np.int16))
except Exception as e:
    print(f"Error occurred: {e}")
finally:
     if 'record' in locals():
        try:
            record.stop()
            record.delete()
            print("Recording stopped.")
        except:
            pass
     if frames:
        audio = np.concatenate(frames, axis=0)
        sf.write(name, audio, samplerate=samplingrate)
        print(f"Recording saved to '{name}'")
     else:
        print("No frames recorded.")
     print("Recording stopped.")

