from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

def prompts(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(input_ids, max_length=512, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Answer:", answer)
modelname="t5-base"
model =T5ForConditionalGeneration.from_pretrained(modelname)
tokenizer = T5Tokenizer.from_pretrained(modelname)

with open(r"D:\coding\intel\ai classroom assistant\transcription\transcripts\t5.txt", "r") as f:

    data = f.read()

choice= int(input("Enter 1 for asking questions, 2 for summarizing: "))

if choice == 1:
    question = input("Enter your question: ")
    input_text = f"question: {question} context: {data}"
    prompts(input_text)
elif choice == 2:
    input_text = f"summarize: {data}"
    summary = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(summary, max_length=300, min_length=200, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Summary:", summary_text)
