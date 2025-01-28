import streamlit as st
import os
from services.chat.get_source import get_info
from services.agents.supervisor import Supervisor
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv(override=True)

agent_list = get_info()

def reset_states():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I am a Talkable Dental Lecture. How can i help?"}]
    st.session_state.intermediate_steps = [[]]
    st.session_state.thread_id = ""

def state_init():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I am a Talkable Dental Lecture. How can i help?"}]

    if "intermediate_steps" not in st.session_state:
        st.session_state.intermediate_steps = [[]]
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = ""
    
    if "agent" not in st.session_state:
        st.session_state.agent = agent_list[0]

    if "agent_model" not in st.session_state:
        st.session_state.agent_model = Supervisor(
            name="Dental RAG", 
            llm=ChatOpenAI(model="gpt-4o", streaming=True),
            embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
            file=agent_list[0]
        )