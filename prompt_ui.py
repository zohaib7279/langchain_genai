import os
import streamlit as st
from google import genai


st.set_page_config(
    page_title="Zohaib Gemini AI Chatbot",
    page_icon="✨",
    menu_items={
        "About": "Zohaib Gemini AI Chatbot powered by Google Gemini"
    }
)


# Theme option
mode = st.sidebar.selectbox(
    "Theme",
    ["Light Mode", "Dark Mode"]
)


if mode == "Dark Mode":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)



def start_chatbot():

    chat = client.chats.create(
        model="gemini-2.5-flash"
    )


    st.title("Gemini Chatbot")


    st.write(
    """
    Zohaib Gemini AI Chatbot is a free AI assistant 
    built using Google Gemini API and Streamlit.
    """
    )



    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        st.write(message)



    # stop button
    if st.session_state.get("loading", False):

        if st.button("⏹ Stop answering"):

            st.session_state.loading = False
            st.rerun()



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


        with st.spinner("✦ Think the Gemini..."):


            last_message = (
                st.session_state
                .messages[-1]
                .replace("You: ", "")
            )


            response = chat.send_message(
                last_message
            )


            st.session_state.messages.append(
                f"✦ Gemini: {response.text}"
            )


        st.session_state.loading = False


        st.rerun()



if __name__ == "__main__":
    start_chatbot()