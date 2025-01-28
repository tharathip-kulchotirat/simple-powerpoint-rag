from pydantic import BaseModel, UUID4
from typing import List

# FOR REQUESTS
class ChatRequestInput(BaseModel):
    input: str

class SessionRequest(BaseModel):
    session_id: str

class ConfigRequest(BaseModel):
    configurable: SessionRequest

class ChatCompletionRequest(BaseModel):
    input: ChatRequestInput
    config: ConfigRequest
    kwargs: dict = {}

# FOR RESPONSE
class ChatObjectResponse(BaseModel):
    content: str
    type: str
    tool_calls: List = None
    invalid_tool_calls: List = None

class ChatResponseOutput(BaseModel):
    input: str
    output: str
    chat_history: List[ChatObjectResponse] = []
    intermediate_steps: List[dict] = []

class ChatMetadataResponse(BaseModel):
    run_id: str = None
    feedback_tokens: List = []

class ChatCompletionResponse(BaseModel):
    output: ChatResponseOutput
    metadata: ChatMetadataResponse