import streamlit as st
from dotenv import load_dotenv
from uuid import uuid4
from services.agents.react_agent import get_graph
import os

# models
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver


load_dotenv(override=True)

@st.cache_resource
def get_thread():
    thread_id = str(uuid4())
    return thread_id

# layout
st.set_page_config(page_title="Talk with Lecture", page_icon="assets/logo.png")


thread_id = get_thread()
# get the graph
llm = ChatOpenAI(model="gpt-4o", streaming=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store_path = "src/assets/vectorstores"
checkpointer = MemorySaver()
graph = get_graph(llm, embeddings, vector_store_path, checkpointer)

# display graph
with st.sidebar:
    st.subheader("Thread ID")
    st.markdown(f"{thread_id}")
    st.subheader("ReAct Agent")
    st.markdown("This is a ReAct agent that uses OpenAI's GPT-4o model to answer questions about dental topics.")
    graph_image = graph.get_graph().draw_mermaid_png()
    st.image(graph_image)

    st.divider()
    st.subheader("My Knowledge")
    files = os.listdir("src/assets/knowledge")
    for file in files:
        st.markdown(f"- {file}")

# state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chatbot
if len(st.session_state.messages) == 0:
    intro_message = "Hi! I am a Talkable Dental Lecture. How can I help?"
    st.session_state.messages.append({"role": "assistant", "content": intro_message})

# Display and render old chat messages
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])

if prompt := st.chat_input("How can I help?"):
    st.session_state.thread_id = thread_id
    st.session_state.messages.append({"role": "human", "content": prompt})
    # invoke the graph
    config = {"configurable": {"thread_id": thread_id}}
    response = graph.invoke({"messages": [("human", prompt)]}, config)

    # update the session state
    st.session_state.messages.append({"role": "human", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response['messages'][-1].content})

    # write the response
    st.chat_message('assistant').write(response['messages'][-1].content)