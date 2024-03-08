import google.generativeai as palm
import streamlit as st
# import random
import time
import prompts
import base64
from huggingface_hub import InferenceClient
import io
# from langchain_google_genai import GoogleGenerativeAI
# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import PromptTemplate

PALM_API_KEY = "AIzaSyA5x8fM-YntTRV_J3wsz6niBLz0u0hpQWc"
client = InferenceClient(model="emilianJR/CyberRealistic_V3", token="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")

palm.configure(api_key=PALM_API_KEY)
model = "models/text-bison-001"

st.title("EDITH")

drawable_synonyms = {"draw", "paint", "image", "picture", "photo", "painting", "drawing", "images"}
is_image_query = False

def img_to_bytes(img_path):
    img_byte_arr = io.BytesIO()
    img_path.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    encoded = base64.b64encode(img_byte_arr).decode()
    return encoded

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
      img_to_bytes(img_path)
    )
    return img_html



if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I'm EDITH, How may I help you?"}]

# Loop Through the Session messages and display it.  
for message in st.session_state.messages:
    if "<img " in message['content']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        if drawable_synonyms.intersection(set(prompt.split(" "))):
            is_image_query = True
            get_image = client.text_to_image(prompt=f"ultra realistic close-up (({prompt})), hyper detail, cinematic lighting, magic neon, Canon EOS R3, nikon, f/1.4, ISO 200, 1/160s, 8K, RAW, unedited, symmetrical balance, in-frame, 8K", negative_prompt="painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",)
        else:
            palm_bot = palm.generate_text(
                        model=model,
                        prompt=prompts.prompt_template05.format(question=prompt),
                        temperature=0.7,
                        # The maximum length of the response
                        max_output_tokens=2000,
                    )

    
    with st.chat_message("assistant"):
        with st.spinner("Generating..."):
            time.sleep(1)
        if is_image_query:
            message_placeholder = st.empty()
            

            image = img_to_html(get_image)
            st.markdown(image, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": image})
        else:
            message_placeholder = st.empty()
            full_response = ""
            for response in palm_bot.result:
                full_response += response
                time.sleep(0.01)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

