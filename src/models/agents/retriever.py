from pydantic import BaseModel

class Retrievers(BaseModel):
    loaded_retrievers: list = []
    loaded_names: list = []
    loaded_descriptions: list = []