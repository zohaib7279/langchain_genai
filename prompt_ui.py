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



    # New chat button
    if st.button("🆕 New Chat"):

        st.session_state.messages = []

        st.rerun()



    # chat session
    if "chat" not in st.session_state:

        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash"
        )



    # messages memory
    if "messages" not in st.session_state:

        st.session_state.messages = []



    # loading state
    if "loading" not in st.session_state:

        st.session_state.loading = False




    # old messages show

    for msg in st.session_state.messages:

        role, text = msg.split(":",1)


        if role == "You":

            with st.chat_message("user"):

                st.write(text)


        else:

            with st.chat_message("assistant"):

                st.write(text)






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






    if st.session_state.loading:


        with st.chat_message("assistant"):


            placeholder = st.empty()


            answer = ""



            try:


                for chunk in st.session_state.chat.send_message_stream(
                    st.session_state.messages[-1].replace(
                        "You:",
                        ""
                    )
                ):


                    answer += chunk.text


                    placeholder.write(answer)




                st.session_state.messages.append(
                    f"Gemini:{answer}"
                )



            except Exception as e:


                st.error(
                    "❌ Gemini se response nahi aa raha. Dobara try karo."
                )


                st.write(e)



        st.session_state.loading = False


        st.rerun()






if __name__ == "__main__":

    start_chatbot()