from langchain.vectorstores import FAISS
from langchain.schema import Document
from typing import List
from loguru import logger

class FAISSVectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_store = None

    def add_documents(self, documents: List[str]):
        """Add processed documents to vector store"""
        try:
            docs = [Document(page_content=text) for text in documents]
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise

    def as_retriever(self):
        """Expose vector store as retriever"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        return self.vector_store.as_retriever()