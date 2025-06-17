# AI-calssroom-assistant
This is a project about an AI classroom assistant that transcribes and summarizes the lecture, creates quizzes, and gives answers to prompts 

For this to run we need ffmpeg installed

as per the current version we are done with the first phase which is recording and transcribing the lecture being recorded

the first one is the logic for the recording of the audio and it uses PVRecorder module which lets us choose the mic and also record and save the file in the folder "recordings"

the second code is the logic for transcribing the recorded file using openai's wishper small model and saves it in a folder called "transcriptions"
