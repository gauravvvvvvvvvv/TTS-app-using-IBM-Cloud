import streamlit as st
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import base64
import os

IBM_API_KEY = st.secrets["IBM_API_KEY"]
IBM_URL = st.secrets["IBM_URL"]

authenticator = IAMAuthenticator(IBM_API_KEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(IBM_URL)

def synthesize_text(text):
    response = tts.synthesize(
        text,
        voice='en-US_AllisonV3Voice',
        accept='audio/wav'
    ).get_result()
    return response.content

def save_audio(content, filename='output.wav'):
    with open(filename, 'wb') as audio_file:
        audio_file.write(content)

def audio_player(audio_file):
    audio_bytes = open(audio_file, 'rb').read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    st.audio(audio_bytes, format='audio/wav')

st.title("IBM Text-to-Speech with Streamlit")

text = st.text_area("Enter text here:")

if st.button("Synthesize"):
    audio_content = synthesize_text(text)
    save_audio(audio_content)
    audio_player('output.wav')
