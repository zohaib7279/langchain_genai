import os
import streamlit as st
from google import genai


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)


def start_chatbot():

    chat = client.chats.create(model="gemini-2.5-flash")

    st.title("🤖 Gemini Chatbot")


    # chat history save karne ke liye
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # purane messages show karna
    for message in st.session_state.messages:
        st.write(message)


    user_message = st.chat_input(
        "Message likho...",
        disabled=st.session_state.get("loading", False)
    )


    if user_message:

        st.session_state.loading = True

        st.session_state.messages.append(
            f"You: {user_message}"
        )

        st.rerun()



    if st.session_state.get("loading", False):

        with st.spinner("🤖 Think the Gemini!"):

            last_message = st.session_state.messages[-1].replace(
                "You: ",
                ""
            )

            response = chat.send_message(last_message)


            st.session_state.messages.append(
                f"🤖 Gemini: {response.text}"
            )


        st.session_state.loading = False

        st.rerun()



if __name__ == "__main__":
    start_chatbot()