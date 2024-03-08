import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css
from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai
import os
from langchain_community.embeddings import GooglePalmEmbeddings
from io import BytesIO
from gtts import gTTS
import base64
import time 
import librosa
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import re

GENAI_API_KEY = "AIzaSyA5x8fM-YntTRV_J3wsz6niBLz0u0hpQWc"
os.environ["GOOGLE_API_KEY"] = GENAI_API_KEY

genai.configure(api_key=GENAI_API_KEY)


########################################Login/SignUp########################################################
if not firebase_admin._apps:
    cred = credentials.Certificate('C:\\Users\\samis\\OneDrive\\Desktop\\DOC Chatbot\\ask-multiple-pdfs-main\\document-chatbot-8b13f-6877f0069a1d.json')
    default_app = firebase_admin.initialize_app(cred)

st.set_page_config(page_title="Chat with multiple PDFs",
                    page_icon=":books:")


if 'username' not in st.session_state:
    st.session_state.username = ''
if 'useremail' not in st.session_state:
    st.session_state.useremail = ''



def f(): 
    try:
        user = auth.get_user_by_email(email)
        print(user.uid)
        st.session_state.username = user.uid
        st.session_state.useremail = user.email
        
        global Usernm
        Usernm=(user.uid)
        
        st.session_state.signedout = True
        st.session_state.signout = True    
        
    except: 
        st.warning('Login Failed')

def t():
    st.session_state.signout = False
    st.session_state.signedout = False   
    st.session_state.username = ''


    

    
if "signedout"  not in st.session_state:
    st.session_state["signedout"] = False
if 'signout' not in st.session_state:
    st.session_state['signout'] = False    
    

    

if  not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
    choice = st.selectbox('Login/Signup',['Login','Sign up'])
    email = st.text_input('Email Address')
    password = st.text_input('Password',type='password')
    

    
    if choice == 'Sign up':
        username = st.text_input("Enter  your unique username")
        
        if st.button('Create my account'):
            user = auth.create_user(email = email, password = password,uid=username)
            
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()
    else:
        # st.button('Login', on_click=f)          
        st.button('Login', on_click=f)
        
        
    
    
##############################################PDF ChatBot###################################################

def get_duration_librosa(file_path):
   audio_data, sample_rate = librosa.load(file_path)
   duration = librosa.get_duration(y=audio_data, sr=sample_rate)
   return duration


def text_to_speech(text):
    """
    Converts text to an audio file using gTTS and returns the audio file as binary data
    """
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang="en")
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = GooglePalmEmbeddings(model="models/embedding-001", google_api_key=GENAI_API_KEY)
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=GENAI_API_KEY)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

if 'doc' not in st.session_state:
    st.session_state['doc'] = False

def handle_userinput(user_question):
    if st.session_state.doc == False:
        st.warning("To Chat, Please Load PDF!")
    elif st.session_state.doc == True:
        try:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            with st.spinner("Generating..."):
                try:
                    system_response =  str(st.session_state.chat_history[-1]).split("content='")[1]
                    print(system_response)
                    system_response = re.sub(r"\\\\.|[^a-zA-Z0-9]+",' ',system_response).replace(" n ", "")
                    print(system_response)
                    # print(system_response.replace(" n ", ""))
                    audio_base64 = base64.b64encode(text_to_speech(system_response)).decode('utf-8')
                    audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
                    with open("ai_resp_audio2.wav", mode="wb") as audio_f:
                        audio_f.write(text_to_speech(system_response))
                    duration = get_duration_librosa("ai_resp_audio2.wav")
                    gif_runner = st.image("ai_6.gif")
                    st.markdown(audio_tag, unsafe_allow_html=True)
                    time.sleep(round(duration))
                    gif_runner.empty()
                except:
                    st.warning("Please Re-Upload File.")
        except:
            st.warning("Give Clear Input To Get The Answer.")
            # st.audio(text_to_speech(system_response), format="audio/wav")
# @st.cache
def main():
    
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:", key='text')
    # generate = st.button("generate")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True, type="pdf")
        print(pdf_docs) 
        if pdf_docs is not None:

            if st.button("Process"):
                st.session_state.doc = True
                with st.spinner("Processing"):
                    # get pdf text
                    raw_text = get_pdf_text(pdf_docs)

                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(
                        vectorstore)
        st.button('Sign out', on_click=t)

if __name__=='__main__':
    if st.session_state.signout:
        main()