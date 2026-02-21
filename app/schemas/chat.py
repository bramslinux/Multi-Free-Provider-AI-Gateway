from pydantic import BaseModel
from typing import List,Dict

class ChatRequest(BaseModel):
    messages:List[Dict]

class ChatResonse(BaseModel):
    provider : str
    response : str