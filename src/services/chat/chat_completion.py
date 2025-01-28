import requests
from pydantic import UUID4
from models.chat_completion import ChatCompletionRequest, ChatRequestInput, SessionRequest, ConfigRequest
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

# models
from langchain_core.runnables import RunnableWithMessageHistory

def complete(agent, input: str, session_id: UUID4 = uuid4()):
    body = ChatCompletionRequest(
        input=ChatRequestInput(input=input),
        config=ConfigRequest(
            configurable=SessionRequest(session_id=str(session_id))
        )
    )

    chain = RunnableWithMessageHistory(
        agent.agent_executor,
        lambda session_id: agent.get_memory(session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    response = chain.invoke(body.input.model_dump(), config=body.config.model_dump())

    if response:
        return response
    else:
        raise Exception(f"Failed to complete chat")