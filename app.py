import time
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_chat import message
st.set_page_config(
    page_title="SkyChat",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)
# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Project: Q&A Chatbot")

# Add custom CSS to set border and font
st.markdown(
    """
    <style>
    .main {
        height:auto;
        width:50%;
        margin:auto;
        border: 2px solid #007BFF; /* Blue border */
        padding: 10px;
        border-radius: 8px;
        max-height: 80vh; /* Maximum height to allow scrolling */
        overflow-y: auto; /* Enable vertical scrolling */
        font-family: 'Arial', sans-serif; /* Change font family */
    }
    .streamlit-expanderHeader {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("👽SkyChat 2.0.0 : gemini version(history)")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask me :)")

if submit and input:
    # Show a spinner while waiting for the response
    with st.spinner("Generating response..."):
      
        response = get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        for chunk in response:
            st.session_state['chat_history'].append(("Bot", chunk.text))
        
        st.toast('Response generated successfully!', icon='✅')

# Display the chat history using the streamlit_chat message function
for role, text in reversed(st.session_state['chat_history']):
    if role == "You":
        message(text, is_user=True)
    else:
        message(text)
