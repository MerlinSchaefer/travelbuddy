import os

import streamlit as st
from dotenv import load_dotenv

# from prompts import ..
# from llm import load_base_LLM, load_chat_LLM

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="TravelBuddy", page_icon=":island:")

st.title("TravelBuddy")
