import streamlit as st
from loguru import logger
from src.ppt_chatbot.data_processing.ppt_parser import PPTParser
from src.ppt_chatbot.llm.chain_manager import ChainManager

class ChatInterface:
    def __init__(self):
        self.parser = PPTParser()
        self.chain_manager = ChainManager()
        
    def render_sidebar(self):
        """Render sidebar file uploader"""
        with st.sidebar:
            st.header("Upload Presentation")
            uploaded_file = st.file_uploader(
                "Choose a PPTX file",
                type=["pptx"],
                accept_multiple_files=False
            )
            return uploaded_file

    def render_chat(self, chain):
        """Main chat interface"""
        st.header("Chat with Presentation")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        if prompt := st.chat_input("Ask about the presentation"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.spinner("Analyzing..."):
                try:
                    response = chain({"question": prompt})
                    answer = response["answer"]
                except Exception as e:
                    logger.error(f"Chat error: {str(e)}")
                    answer = "Sorry, I encountered an error processing your request."
                
                with st.chat_message("assistant"):
                    st.markdown(answer)
                
                st.session_state.messages.append({"role": "assistant", "content": answer})