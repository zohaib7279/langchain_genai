import os
import streamlit as st
from google import genai


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)


def start_chatbot():

    chat = client.chats.create(model="gemini-2.5-flash")

    st.title("🤖 Gemini Chatbot")


    user_message = st.chat_input("Message likho...")


    if user_message:

        st.write("You:", user_message)


        response = chat.send_message(user_message)


        st.write("🤖 Gemini:", response.text)



if __name__ == "__main__":
    start_chatbot()