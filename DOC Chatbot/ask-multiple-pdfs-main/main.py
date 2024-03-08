HUGGINGFACEHUB_API_TOKEN= "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"

import textwrap
import getpass
import os
import numpy as np
import pandas as pd

import google.generativeai as genai
import google.ai.generativelanguage as glm
GENAI_API_KEY = "AIzaSyA5x8fM-YntTRV_J3wsz6niBLz0u0hpQWc"
os.environ["GOOGLE_API_KEY"] = GENAI_API_KEY

genai.configure(api_key=GENAI_API_KEY)

# for m in genai.list_models():
#   if 'embedContent' in m.supported_generation_methods:
#     print(m.name)

# sample_text = ("Hello world")

# model = 'models/embedding-001'
# embedding = genai.embed_content(model=model,
#                                 content=sample_text,
#                                 task_type="retrieval_document",
#                                 )

# print(f"genai embedding: {embedding['embedding'][:5]}")


# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# vector = embeddings.embed_query("hello world")
# print(f"langchain genai embedding: {vector[:5]}")

# from langchain_google_genai import GoogleGenerativeAI
# llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=GENAI_API_KEY)
# print(
#     llm.invoke(
#         "What are some of the pros and cons of Python as a programming language?"
#     )
# )
# from PyPDF2 import PdfReader
# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         print(pdf)
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# print(get_pdf_text(["resume.pdf"]))
# import mutagen 
# from mutagen.wave import WAVE 
# def audio_duration(length): 
#     hours = length // 3600  # calculate in hours 
#     length %= 3600
#     mins = length // 60  # calculate in minutes 
#     length %= 60
#     seconds = length  # calculate in seconds 
  
#     return hours, mins, seconds  # returns the duration 

# audio = WAVE("ai_resp_audio.wav") 

# # contains all the metadata about the wavpack file 
# audio_info = audio.info 
# length = int(audio_info.length) 
# hours, mins, seconds = audio_duration(length) 
# print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))

# import wave
# def get_duration_wave(file_path):
#    with wave.open(file_path, 'r') as audio_file:
#       frame_rate = audio_file.getframerate()
#       n_frames = audio_file.getnframes()
#       duration = n_frames / float(frame_rate)
#       return duration
# file_path = 'ai_resp_audio2.wav'
# duration = get_duration_wave(file_path)
# print(f"Duration: {duration:.2f} seconds")

# import librosa
# def get_duration_librosa(file_path):
#    audio_data, sample_rate = librosa.load(file_path)
#    duration = librosa.get_duration(y=audio_data, sr=sample_rate)
#    return duration
# file_path = 'ai_resp_audio.wav'
# duration = get_duration_librosa(file_path)
# print(f"Duration: {round(duration)} seconds")
# import time

# start = time.time()
# i = 0
# while range(20):
#    print(i+1)

# end = time.time()

# print(start-end)

import re
string = "Data Science Intern, Pranaksh Infotech\nML/DL ENGINEER AND DATA SCIENTIST"

n_str = re.sub(r"[^a-zA-Z0-9]+",' ',string)

print(n_str)