import streamlit as st
from services.chat.chat_completion import complete
from services.chat.get_source import get_info
from dotenv import load_dotenv
from states.state_init import state_init, reset_states
from services.slides.get_slide import get_slide
from uuid import uuid4

# models
from services.agents.supervisor import Supervisor
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv(override=True)

state_init()

# layout
st.set_page_config(page_title="Talk with Lecture", page_icon="assets/logo.png")

# SIDEBAR
with st.sidebar:
    _, mid_image, _ = st.columns((1, 2, 1))
    with mid_image:
        st.image("src/assets/logo.png", width=120)
    st.markdown("# Talk with Lecture", unsafe_allow_html=True)

    agent_list = get_info()
    agent = st.selectbox("Choose file", sorted(agent_list), on_change=reset_states)

    # TODO !! <<< how can user choose agent, then pass to supervisor
    # if the agent changed, reset the session state
    if agent != st.session_state.agent:
        st.session_state.agent = agent
        st.session_state.agent_model = Supervisor(
            name="Dental RAG", 
            llm=ChatOpenAI(model="gpt-4o", streaming=True),
            embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
            file=agent
        )


# Chatbot
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        steps = st.session_state.intermediate_steps[i]
        if len(steps) > 0 and message["role"] == 'assistant':
            with st.expander(f"Citations:", expanded=False):
                for step in steps:
                    st.markdown("**I used** " + step['tool'].upper() + " for my source.")
                    st.markdown(f"**My Input:** {step['tool_input']}")
                    st.json(f"""
                                {step.get('metadata', step.get('content', 'No Metadata Provided'))[0]}
                                """)
                    slide_number = step['metadata'][0].get('slide_number')
                    slide = get_slide(agent, slide_number)
                    st.image(slide)

if prompt := st.chat_input("Hi! I am a Talkable Dental Lecture. How can i help?"):

    if len(st.session_state.messages) == 1:
        st.session_state.session_id = str(uuid4())

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.intermediate_steps.append([])

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = complete(agent=st.session_state.agent_model, input=prompt, session_id=st.session_state.session_id)
            content = result['output']
            response = st.markdown(content)
            steps = result['intermediate_steps']
        if len(steps) > 0:
            with st.expander(f"Citations:", expanded=False):
                for step in steps:
                    st.markdown("**I used** " + step[0].tool.upper() + " for my source.")
                    st.markdown(f"**My Input:** {step[0].tool_input}")
                    st.json(f"""
                                {step[1].get('metadata', step[1].get('content', 'No Metadata Provided'))[0]}
                                """)
                    slide_number = step[1].get('metadata')[0].get('slide_number')
                    slide = get_slide(agent, slide_number)
                    st.image(slide)
            
            st.session_state.intermediate_steps.append([{"tool": step[0].tool.upper(),"tool_input": step[0].tool_input,"metadata": step[1].get('metadata', step[1].get('content', 'No Metadata Provided'))} for step in steps])
        else:
            st.session_state.intermediate_steps.append([])
    st.session_state.messages.append({"role": "assistant", "content": content})   