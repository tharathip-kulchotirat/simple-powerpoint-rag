# Agent services
from services.agents.member import Member

# langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.chat_message_histories import SQLChatMessageHistory

# Runnables
from langchain_core.chat_history import BaseChatMessageHistory

# Tools
from sqlalchemy import create_engine

class Supervisor:
    def __init__(self, name, llm, embeddings, file):
        self.name = name
        self.llm = llm
        self.file = file
        self.embeddings = embeddings
        self.chains = []
        self.chain_names = []
        self.chain_descriptions = []
        self.tools = []
        self.memory = None
        self.conn = None
        self.memory_table_name = "chat_history"

        # 1-get tools
        self._get_tools()
        self._memory_conn()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    "You are a helpful dental lecture assistant developed by Dr.Tharathip Kulchotirat, designed to assist with a wide range of tasks using the tools provided. You generate human-like, coherent, and relevant responses based on the input you receive."
                    "You do not rely on any background knowledge and only use the provided tools for answering questions. When a question relates to the tools available, always utilize the tools to ensure precision and accuracy. For questions not related to the tools, respond with a statement such as, 'I have no background knowledge to answer this.'"
                    "TOOLS:"
                    "------"
                    "You have access to the following tools:"
                    f"{self.chain_names}"
                    "Begin!"
                    "The final answer is:"
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        self._build_supervisor()
    
    def _get_tools(self):
        chain = Member(llm=self.llm, embeddings=self.embeddings, file=self.file)
        chains = chain.create_chains()
        self.chains += chains.chains
        self.chain_names += chains.chain_names
        self.chain_descriptions += chains.chain_descriptions
        self.tools += chains.chain_as_tools

    def _memory_conn(self):
        # Prepare checkpoints
        try:
            self.conn = create_engine(url='sqlite:///memory.db')
                
        except (ValueError, ConnectionError) as e:
            raise RuntimeError(
                f"Failed to load memory checkpoint. Ensure configuration and connection details are correct. Error: {e}"
            ) from None
        
        except Exception as e:
            raise Exception(f"Error loading memory checkpoint: {e}") from None
    
    def get_memory(self, session_id: str) -> BaseChatMessageHistory:
        """
        Get the memory for a given session ID.
        """
        if self.conn is not None:
            self.memory = SQLChatMessageHistory(
                table_name=self.memory_table_name,
                session_id=session_id,
                connection=self.conn
            )
        else:
            from langchain_core.chat_history import InMemoryChatMessageHistory
            self.memory = InMemoryChatMessageHistory(session_id=session_id)
            
        return self.memory

    def _build_supervisor(self):
        """
        Build the a supervisor.
        """
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, return_intermediate_steps=True, max_iterations=5, early_stopping_method="force", handle_parsing_errors=True)
        self.agent_executor = agent_executor