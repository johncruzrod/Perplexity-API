import streamlit as st
import requests
import json

# Function to call the Perplexity API
def call_api(model_name, conversation_messages):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": model_name,
        "messages": conversation_messages
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {st.secrets['PERPLEXITY_API_KEY']}"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def update_messages(user_input):
    st.session_state['messages'].append({"role": "user", "content": user_input})
    response = call_api("sonar-medium-online", [{"role": "user", "content": user_input}])
    if 'error' not in response:
        assistant_reply = response['choices'][0]['message']['content']  # Adjust this according to actual API response format
        st.session_state['messages'].append({"role": "assistant", "content": assistant_reply})
    else:
        st.error("Error: " + response["error"])
    # Force a rerun to update the chat messages immediately
    st.experimental_rerun()

# Initialize the chat session
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Chat with AI')

# Display past messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new messages
user_input = st.chat_input("Ask something...")
if user_input:
    update_messages(user_input)
