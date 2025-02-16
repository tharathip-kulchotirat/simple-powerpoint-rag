from src.services.agents.react_agent import get_graph
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOpenAI(model="gpt-4o", streaming=True)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store_path = "src/assets/vectorstores"
checkpointer = MemorySaver()

graph = get_graph(llm, embeddings, vector_store_path, checkpointer)
config = {"configurable": {"thread_id": "1423"}}
print(graph.invoke({"messages": [("human", "What's the proper torque for dental implants?")]}, config))