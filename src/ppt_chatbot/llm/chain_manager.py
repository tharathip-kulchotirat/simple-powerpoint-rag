from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from src.ppt_chatbot.llm.vector_store import FAISSVectorStore
from loguru import logger
import os

class ChainManager:
    def __init__(self, api_key: str = None):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        self.llm = OpenAI(
            temperature=0.7,
            max_tokens=1500,
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )

    def create_chain(self, documents: list[str]):
        """Create conversational QA chain"""
        try:
            vector_store = FAISSVectorStore(self.embeddings)
            vector_store.add_documents(documents)
            
            return ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vector_store.as_retriever(),
                memory=self.memory,
                verbose=True
            )
        except Exception as e:
            logger.error(f"Chain creation failed: {str(e)}")
            raise