import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# .env file se API key load karo
load_dotenv()

st.title("AI Research Tool")

# ✅ PEHLE: Model dropdown (UPER)
model_options = [ 
    "gemini-2.5-pro",
    "gemini-2.0-flash-exp"
]
selected_model = st.selectbox("Select Model", model_options)

# ✅ PHIR: Research Topic (NEECHE)
topic = st.text_area("Research Topic", height=100)

# ✅ SAB SE NEECHE: Button
if st.button("Research"):
    if not topic:
        st.warning("Please enter a research topic!")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("API key not found in .env file! Please add GOOGLE_API_KEY=your_key in .env")
    else:
        try:
            # Model initialize karo - API key .env se
            llm = ChatGoogleGenerativeAI(
                model=selected_model,  # Dropdown se select ho raha hai
                google_api_key=os.getenv("GOOGLE_API_KEY")  # .env se auto load
            )
            
            # Response generate karo
            response = llm.invoke(f"Research topic: {topic}")
            
            # Response show karo
            st.success("Research Complete!")
            st.write(response.content)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")