
import speech_recognition as sr
import streamlit as st
import subprocess

from agent import sql_generater
from db import get_data
from templates import navbar,background_style,rewrite_default_css,question_template,response_template

st.markdown(navbar, unsafe_allow_html=True)

# Function to transcribe audio
def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    try:
        # Using Google's speech recognition API to transcribe audio
        text = recognizer.recognize_google(audio)
        return True, text
    except sr.UnknownValueError:
        return False , "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return False , "Sorry, I couldn't request results from Google Speech Recognition service."

# Function to capture longer voice input
def capture_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Create placeholders for messages
        listening_placeholder = st.empty()  # This will be used to show "Listening"
        processing_placeholder = st.empty()  # This will show "Processing"
        
        # Show the "Listening for your voice..." message
        listening_placeholder.write("Listening...")

        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        transcription = None
        try:
            # Setting a timeout and phrase_time_limit for longer input
            audio = recognizer.listen(source, timeout=60, phrase_time_limit=60)  # 60 seconds limit
            listening_placeholder.empty()  
            processing_placeholder.write("Processing...")
            
            # Send the audio to the transcription function
            is_okay, transcription = transcribe_audio(audio)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            processing_placeholder.empty() 
        
            return is_okay, transcription



# Initialize session state if not already present

if 'user_queries' not in st.session_state:
    st.session_state.user_queries = []

if 'responses' not in st.session_state:
    st.session_state.responses = []

# if "is_processing" not in st.session_state:
#     st.session_state.is_processing = False



def get_conversation_history(top_k=5):
    num_conversations = len(st.session_state.user_queries)

    # Check if there are conversations stored
    if num_conversations == 0:
        return ""  

    # Split into newer (top 3) and older conversations
    newer_conversations = list(zip(st.session_state.user_queries[-top_k:], st.session_state.responses[-top_k:]))
    older_conversations = st.session_state.user_queries[:-top_k]  # All older questions

    # Format the newer conversations (both question and answer)
    newer_text = ""
    for idx, (question, answer) in enumerate(newer_conversations):
        newer_text += f"Q{len(st.session_state.user_queries) - len(newer_conversations) + idx + 1}: {question}\n"
        newer_text += f"A{len(st.session_state.responses) - len(newer_conversations) + idx + 1}: {answer}\n"
        newer_text += "---\n"

    # Format the older conversations (only questions)
    older_text = ""
    for idx, question in enumerate(older_conversations):
        older_text += f"Q{len(st.session_state.user_queries) - len(older_conversations) + idx + 1}: {question}\n"
        older_text += "---\n"

    return older_text +"\n"+ newer_text


def chat_page():
    st.markdown(background_style, unsafe_allow_html=True)
    st.markdown(rewrite_default_css, unsafe_allow_html=True)


    col1, col2 = st.columns([6, 1])  

    
    # Create a text input field in the first column
    text_input = col1.chat_input(placeholder="Enter text here:")
    mic_emoji = "🎙️"  # Microphone emoji
    with col2:
        is_okay = True

        if st.button(mic_emoji, key="mic_button"):
            is_okay,transcription = capture_voice_input()
            if transcription:
                text_input = text_input + " " + transcription if text_input else transcription

    if text_input:

        print("user q:",text_input)

        st.markdown(question_template(text_input) , unsafe_allow_html=True)
        st.session_state.user_queries.append(text_input)
        if is_okay:
            # st.write(st.status())
            with st.spinner(""):
                query,response = sql_generater(text_input,get_conversation_history())
            st.session_state.responses.append(response)
            st.markdown(response_template(response), unsafe_allow_html=True)
        else:
            response =  "Sorry, I couldn't understand the audio."
            is_okay = True
        


    if st.session_state.user_queries:
        
        # Reverse the list to show the latest conversation first
        for idx, (question, response) in enumerate(reversed(list(zip(st.session_state.user_queries, st.session_state.responses)))): 
            if idx ==0:
                continue
            st.markdown(question_template(question) , unsafe_allow_html=True)
            st.markdown(response_template(response), unsafe_allow_html=True)





if __name__ == "__main__":
    chat_page()


