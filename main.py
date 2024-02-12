from google.cloud import dialogflow_v2beta1 as dialogflow
import os
from datetime import datetime, timedelta
import streamlit as st

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "zhie.json"

# Replace with your project ID and service account key path
project_id = "zhie-vwxm"
session_id = "1234567"
language_code = "en"

# Create a Dialogflow session client
session_client = dialogflow.SessionsClient()

# Define a function to send text and receive response
def detect_intent_text(text):
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    # var1 = response.query_result.parameters["date"] if response.query_result.parameters else None
    # var2 = response.query_result.parameters["time"] if response.query_result.parameters else None
    # print(var1, var2)

    # if var1 != None and var2 != None:
    #     dt = datetime.strptime(var1, "%Y-%m-%dT%H:%M:%S%z")
    #     # Convert to local time (assuming PST in this case)
    #     local_dt = dt - timedelta(hours=8)
    #     # Format in various human-readable styles
    #     print(local_dt.strftime("%B %d, %Y at %I:%M %p (%Z)"))

    return response.query_result.fulfillment_text

st.title("Chatbot")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    bot_response = detect_intent_text(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})


