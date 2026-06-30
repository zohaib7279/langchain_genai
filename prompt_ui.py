import os
import streamlit as st
from google import genai


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)



def start_chatbot():

    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon="🤖"
    )


    st.title("🤖 Gemini Chatbot")



    if "chat" not in st.session_state:

        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash"
        )



    if "messages" not in st.session_state:

        st.session_state.messages = []



    if "loading" not in st.session_state:

        st.session_state.loading = False




    # purane messages

    for message in st.session_state.messages:

        role, text = message.split(":",1)


        if role == "You":

            with st.chat_message("user"):
                st.write(text)


        else:

            with st.chat_message("assistant"):
                st.write(text)





    # input disable jab Gemini soch raha ho

    user_message = st.chat_input(
        "Message likho...",
        disabled=st.session_state.loading
    )





    if user_message:


        st.session_state.loading = True


        st.session_state.messages.append(
            f"You:{user_message}"
        )


        st.rerun()





    # Gemini response

    if st.session_state.loading:


        with st.chat_message("assistant"):


            with st.spinner("🤖 Gemini soch raha hai..."):


                placeholder = st.empty()


                full_response = ""



                try:


                    stream = st.session_state.chat.send_message_stream(
                        st.session_state.messages[-1].replace(
                            "You:",
                            ""
                        )
                    )



                    for chunk in stream:


                        full_response += chunk.text


                        placeholder.write(
                            full_response
                        )





                    st.session_state.messages.append(
                        f"Gemini:{full_response}"
                    )



                except Exception as e:


                    st.error(
                        "❌ Error aa gaya"
                    )

                    st.write(e)





        st.session_state.loading = False


        st.rerun()





if __name__ == "__main__":

    start_chatbot()