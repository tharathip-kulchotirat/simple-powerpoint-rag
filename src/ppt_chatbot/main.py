from src.ppt_chatbot.interface.streamlit_ui import ChatInterface
from src.ppt_chatbot.utils.logging import configure_logging
import streamlit as st
from src.ppt_chatbot.data_processing.ppt_parser import PPTParser
from src.ppt_chatbot.llm.chain_manager import ChainManager
from dotenv import load_dotenv
load_dotenv()

def main():
    configure_logging()
    interface = ChatInterface()
    
    uploaded_file = interface.render_sidebar()
    
    if uploaded_file:
        if uploaded_file.size > 500 * 1024 * 1024:
            st.error(f"File size exceeds {500}MB limit")
            return
        
        parser = PPTParser()
        chain_manager = ChainManager()
        
        with st.spinner("Processing presentation..."):
            chunks = parser.parse_pptx(uploaded_file)
            qa_chain = chain_manager.create_chain(chunks)
            interface.render_chat(qa_chain)

if __name__ == "__main__":
    main()