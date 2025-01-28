from pydantic import BaseModel
from typing import List

class ChainOutput(BaseModel):
    chains: list = []
    chain_as_tools: list = []
    chain_names: List[str] = []
    chain_descriptions: List[str] = []
    