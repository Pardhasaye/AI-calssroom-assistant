import streamlit as st
import whisper # Whisper model for transcription
import os
from transformers import pipeline # question-answering pipeline
from transformers import BartTokenizer, BartForConditionalGeneration # For summarization
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer # for quiz generation
import random
from datetime import datetime

# Cache the Whisper model to avoid reloading on every rerun
@st.cache_resource
def whisper_model_small():
    return whisper.load_model("small")
transcribe_model = whisper_model_small()

@st.cache_resource
def bart_large_cnn_model():
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    return tokenizer, model
summary_tokenizer, summary_model = bart_large_cnn_model()

@st.cache_resource
def bart_qa_model():
    return pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
question_answering_model = bart_qa_model()

@st.cache_resource
def t5_small_qg_model():
    model = AutoModelForSeq2SeqLM.from_pretrained("valhalla/t5-small-qa-qg-hl")
    tokenizer = AutoTokenizer.from_pretrained("valhalla/t5-small-qa-qg-hl")
    return model, tokenizer

@st.cache_resource
def ner_distractor_model():
    return pipeline("ner", grouped_entities=True)

quiz_model, quiz_tokenizer = t5_small_qg_model()
ner_distractor_pipeline = ner_distractor_model()

def quiz_generator(text, num_of_questions=5):
    entities = ner_distractor_pipeline(text)
    answers = list({e['word'] for e in entities if e['entity_group'] in ['PER', 'ORG', 'LOC', 'DATE', 'MISC', 'NUMBER']})
    answers = answers[:num_of_questions]
    questions = []

    for ans in answers:
        if ans in text:
            prompt = f"highlight: {text.replace(ans, f'<hl> {ans} <hl>')}"
            input_ids = quiz_tokenizer(prompt, return_tensors="pt").input_ids
            output_ids = quiz_model.generate(input_ids, max_length=128)
            question = quiz_tokenizer.decode(output_ids[0], skip_special_tokens=True)

            # Generate distractors (simple shuffle from other answers)
            distractors = random.sample([a for a in answers if a != ans], k=min(3, len(answers)-1))
            options = distractors + [ans]
            random.shuffle(options)

            questions.append({"question": question, "correct": ans, "options": options})
    return questions

# Folder to save recordings
Folder_Path = "recordings"
os.makedirs(Folder_Path, exist_ok=True)

# Record or upload audio using Streamlit's audio_input
input_audio_file = st.audio_input("Start the recording")  # Use Streamlit's audio_input
st.write("**NOTE**: record as long as possible to generate rich summaries and quizzes")
# Save new recording if it's not a duplicate
if input_audio_file is not None:
    # Get the content of the uploaded/recorded audio file
    file_content = input_audio_file.getbuffer()
    saved = False
    # Check if this file (by content) already exists in the folder
    # Loop through all existing .wav files in the recordings folder
    for exist in os.listdir(Folder_Path):
        if exist.endswith(".wav"):
            # Open each file in binary mode and compare its content to the new file
            with open(os.path.join(Folder_Path, exist), "rb") as f:
                if f.read() == file_content:
                    # If a match is found, mark as saved (duplicate) and break
                    saved = True
                    break

    # If not a duplicate, save the audio file with a timestamped filename
    if not saved:
        # Generate a timestamped filename for the new recording
        timestamp_name = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        save_audio_path = os.path.join(Folder_Path, f"recording_{timestamp_name}.wav")
        with open(save_audio_path, "wb") as f:
            f.write(file_content)
        st.success(f"Audio saved: `{save_audio_path}`")

# List and play existing audio files
exist_files = [f for f in os.listdir(Folder_Path) if f.endswith(".wav")]
if exist_files:
    file_selected = st.selectbox("Select a recording:", sorted(exist_files, reverse=True))
    file_path = os.path.join(Folder_Path, file_selected)
    st.audio(file_path)

    if st.button("submit"):
        with st.spinner("Loading...."):
            st.session_state.transcribed_text = transcribe_model.transcribe(file_path)["text"]
        st.write("**Transcription:**")
        st.write(st.session_state.transcribed_text)

else:
    st.info("-- No recordings found --.")

if "transcribed_text" in st.session_state:
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            input_text = f"{st.session_state.transcribed_text}"
            input_ids = summary_tokenizer(input_text, return_tensors="pt", truncation=True, max_length=1024).input_ids
            outputs = summary_model.generate(input_ids, max_length=150)
            summary = summary_tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.subheader("Summary")
        st.write(summary)


if "transcribed_text" in st.session_state:     # q&a section
    input_question = st.text_input("Enter your question:")

    if st.button("**Ask**"):
        with st.spinner("Finding the answer..."):
            final_result = question_answering_model(
                question=input_question,
                context=st.session_state.transcribed_text
            )
            output_answer = final_result["answer"]
        st.write("**Answer:**")
        st.write(output_answer)
else:
    st.info("Transcribe an audio file first to enable Q&A.")


if "transcribed_text" in st.session_state:
    if st.button("🧪 Generate Quiz"):
        with st.spinner("Generating questions..."):
            st.session_state.quiz_data = quiz_generator(st.session_state.transcribed_text)
            st.session_state.quiz_submitted = False

if "quiz_data" in st.session_state and not st.session_state.get("quiz_submitted", False):
    with st.form("quiz_form"):
        st.subheader(" Take the Quiz")
        user_answers = []
        for i, item in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{i+1}: {item['question']}**")
            selected = st.radio("Select one:", item["options"], key=f"q{i}")
            user_answers.append(selected)
        if st.form_submit_button("Submit Quiz"):
            st.session_state.user_answers = user_answers
            st.session_state.quiz_submitted = True

if st.session_state.get("quiz_submitted", False):
    st.subheader("**Review**")
    score = 0
    for i, (user_ans, item) in enumerate(zip(st.session_state.user_answers, st.session_state.quiz_data)):
        st.markdown(f"**Q{i+1}: {item['question']}**")
        st.markdown(f"- Your Answer: {user_ans}")
        st.markdown(f"- Correct Answer: {item['correct']}")
        if user_ans == item["correct"]:
            st.success("Correct!")
            score += 1
        else:
            st.error("Incorrect.")
        st.markdown("---")
    st.write("**Result**")
    st.success(f" Your Score: {score} / {len(st.session_state.quiz_data)}")

if st.button("Debug NER"):
    entities = ner_distractor_pipeline(st.session_state.transcribed_text)
    st.write("Named Entities Found:")
    st.json(entities)
