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


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=GEMINI_API_KEY
)



def start_chatbot():


    chat = client.chats.create(
        model="gemini-2.5-flash"
    )



    # Session states

    if "messages" not in st.session_state:
        st.session_state.messages = []


    if "loading" not in st.session_state:
        st.session_state.loading = False


    if "stop" not in st.session_state:
        st.session_state.stop = False






    # Sidebar

    if st.sidebar.button("➕ New Chat"):

        st.session_state.messages = []

        st.session_state.loading = False

        st.session_state.stop = False

        st.rerun()




    # Theme

    mode = st.sidebar.selectbox(
        "Theme",
        ["Light Mode", "Dark Mode"]
    )



    if mode == "Dark Mode":

        st.markdown(
            """
            <style>

            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"],
            [data-testid="stSidebar"] {

                background-color:#0e1117;

                color:white;

            }


            .stMarkdown {

                color:white;

            }


            </style>
            """,

            unsafe_allow_html=True
        )



    else:


        st.markdown(
            """
            <style>


            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"],
            [data-testid="stSidebar"] {


                background-color:white;

                color:black;


            }



            .stMarkdown {


                color:black;


            }



            </style>
            """,

            unsafe_allow_html=True
        )







    st.title("Gemini Chatbot")



    st.write(
        """
        Zohaib Gemini AI Chatbot is a free AI assistant
        built using Google Gemini API and Streamlit.
        """
    )







    # Old messages show

    for message in st.session_state.messages:

        st.write(message)







    # Stop button


    if st.session_state.loading:


        if st.button("⏹ Stop answering"):


            st.session_state.stop = True

            st.session_state.loading = False

            st.rerun()







    # Chat input


    user_message = st.chat_input(

        "Message likho...",

        disabled=st.session_state.loading

    )






    if user_message:


        st.session_state.loading = True

        st.session_state.stop = False



        st.session_state.messages.append(

            f"You: {user_message}"

        )


        st.rerun()







    # Gemini streaming response


    if st.session_state.loading:



        last_message = (

            st.session_state.messages[-1]

            .replace("You: ","")

        )



        response_box = st.empty()


        response_text = ""





        with st.spinner("✦ Think the Gemini..."):



            for chunk in chat.send_message_stream(last_message):


                if st.session_state.stop:


                    break



                response_text += chunk.text



                response_box.write(

                    f"✦ Gemini: {response_text}"

                )







        if response_text:


            st.session_state.messages.append(

                f"✦ Gemini: {response_text}"

            )





        st.session_state.loading = False


        st.rerun()






if __name__ == "__main__":

    start_chatbot()