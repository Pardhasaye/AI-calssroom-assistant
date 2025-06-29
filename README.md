# AI-classroom-assistant

This is a project about an AI classroom assistant that transcribes , summarizes the lecture, creates quizzes, and gives answers to prompts from the recoreded classroom session

**MODELS**:

- Transcription --- [`openai/whisper-small`](https://huggingface.co/openai/whisper-small)

- Summarization --- [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn)

- Question and Answering chat --- [`bert-large-uncased-whole-word-masking-finetuned-squad`](https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad)

- Quiz generation --- [`valhalla/t5-small-qa-qg-hl`](https://huggingface.co/valhalla/t5-small-qa-qg-hl) + NER pipeline from Hugging Face (distractor for multiple choice questions)

we used **streamlit** for user interface

- **NOTE:** all models are pre-trained from hugging face

## Transcription

In this phase, our AI classroom assistant converts spoken audio (**recorded audio**) from your classroom into written text.

Model used: [`openai/whisper-small`](https://huggingface.co/openai/whisper-small)

- if there is any existing audio then you can select the audio

  - Transcribe it into text after selecting the audio(directly)
  - Summarize the transcript
  - Generate quizzes from it

- the audio files which are recorded will be saved to recordings folder with timestamp

- the audio file (.wav) will be downloaded in recordings folder as
  **recording_YYYY.MM.DD_HH.MM.SS.wav** format

  - There is a dropdown to view and select saved audio files, so you can:
  - Reuse past recordings
  - Or record new audio directly in the app

> **NOTE:** make sure that the classroom is quiet when using

## Summarization

After the audio is transcribed, the assistant can generate a **concise summary** of the lecture.

**Model used:** [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn)

- Converts the full transcript into a shorter, easier-to-read version (only english)
- Helps quickly understand the main points of a long lecture (works good 10+ minutes)
- Especially useful when the class duration is long or the transcript is large
- Just click the **“Summarize”** button to see the summary

> Summarization works best on clean and sufficiently long transcripts.  
> For very short recordings, the summary might be brief or similar to the transcript.

## Question and answering

- After transcribing the lecture, the assistant can answer your custom questions based on the content or transcribed text

> we are using **transcribed text** for question and answers chat and summarization

Model used: [`bert-large-uncased-whole-word-masking-finetuned-squad`](https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad)

**Works as an open-book assistant:**

- You can type any question about the transcript, and it will find the best matching answer.

Especially useful if you:

- Missed a part of the lecture

- Want to check facts quickly

Just enter your question in the input box and click **"Ask"**

The assistant scans the entire transcript context and returns the most relevant answer

> NOTE:
> The quality of answers depends on the transcript quality.
> Clear, detailed transcripts give better answers.

## Quiz Generation

After transcribing and summarizing, the assistant can automatically create multiple-choice quizzes to help test your understanding of the lecture.

Models used: [`valhalla/t5-small-qa-qg-hl`](https://huggingface.co/valhalla/t5-small-qa-qg-hl) → creates questions

- Hugging Face NER pipeline → extracts key entities to use as answers & distractors

**working:**

- Finds important entities (people, dates, terms) from the transcript

- Generates questions where the correct answer is that entity

- Creates distractors (wrong but similar-looking answers) using other entities

- Presents the quiz as multiple-choice, directly in the Streamlit interface

**Features:**

- After clicking " Generate Quiz", a quiz is created on the fly

- Users can select answers and submit the quiz

- At the end, the assistant:

  - Shows your score

  - Marks which answers were correct or incorrect

## Installation & Running Instructions

- Clone this repository

  > git clone https://github.com/yourusername/ai-classroom-assistant.git

  > cd ai-classroom-assistant

- Create a virtual environment
  > python -m venv (.venv) name it as you like
- Activate the virtual environment

  - Windows:
    > .venv\Scripts\activate
  - macOS/Linux:
    > .venv/bin/activate

- install the required packages:
  - streamlit
  - torch
  - torchaudio
  - transformers
  - openai-whisper
  - openvino
- Directly from the requirements.txt file:

  > pip install -r requirements.txt

- Run the file filename.py(e.g.,Assistant.py):
  > streamlit run Assistant.py
