from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain import hub
from langchain_community.vectorstores import FAISS

# models
from models.agents.member import ChainOutput
from models.agents.retriever import Retrievers

# configs
import os

class Member:
    def __init__(self,llm, embeddings, file):
        self.llm = llm
        self.embeddings = embeddings
        self.file = file
        
        self.retrievers: Retrievers = self._create_retrievers(self.embeddings)
        self.prompt = hub.pull("rlm/rag-prompt")

    def _format_docs(self, docs):
        """
        formats the documents into a single string.
        """
        return "\n\n".join(doc.page_content for doc in docs)
    
    def _format_string(self, input_string):
        """
        Formats a string by converting it to lowercase, replacing spaces, dots, and dashes with underscores.

        Args:
            input_string (str): The input string to format.

        Returns:
            str: The formatted string.
        """
        if not isinstance(input_string, str):
            raise ValueError("Input must be a string.")
            
        # Convert to lowercase
        formatted_string = input_string.lower()
        # Replace spaces, dots, and dashes with underscores
        formatted_string = formatted_string.replace(" ", "_").replace(".", "_").replace("-", "_")
        return formatted_string
    
    def _get_metadata(self, docs):
        """
        gets metadata from the documents.
        """
        return [doc.metadata for doc in docs]

    def _create_retrievers(self, embeddings) -> Retrievers:
        """
        creates retrievers based on the configuration.
        """

        loaded_retrievers = []
        loaded_names = []
        loaded_descriptions = []
        loaded_faiss = FAISS.load_local('src/assets/vectorstores/', embeddings, allow_dangerous_deserialization=True)
        # Test to confirm if the vector store is working correctly.
        loaded_retrievers.append(loaded_faiss.as_retriever(
            search_kwargs={"filter": {"file": self.file}},

        ))
        loaded_names.append(self._format_string(self.file))
        loaded_descriptions.append(self.file)

        return Retrievers(
            loaded_retrievers=loaded_retrievers,
            loaded_names=loaded_names,
            loaded_descriptions=loaded_descriptions
        )

    def create_chains(self) -> ChainOutput:
        """
        creates rag chains
        """

        chains = []

        retrievers = self.retrievers
        vector_stores = retrievers.loaded_retrievers
        chain_names = retrievers.loaded_names
        chain_descriptions = retrievers.loaded_descriptions

        for retriever in vector_stores:
            rag_chain = (
                RunnableParallel(metadata=retriever | self._get_metadata, context=retriever | self._format_docs, question=RunnablePassthrough())
                | RunnablePassthrough.assign(prompt=self.prompt)
                | RunnablePassthrough.assign(response=lambda inputs: self.llm.invoke(inputs["prompt"].messages))
            )
            chains.append(rag_chain)

        as_tools = [chain.as_tool(name=chain_names[i], description=chain_names[i]) for i, chain in enumerate(chains)]

        return ChainOutput(
            chains=chains,
            chain_as_tools=as_tools,
            chain_names=chain_names,
            chain_descriptions=chain_descriptions
        )