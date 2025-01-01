from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Chat:
    _id: ObjectId
    scenario: str
    action: str
    status: str
    last_modified: float
    messages: list[dict]
    patient_id: ObjectId

class BotResponse(BaseModel):
    content: str
    is_over: bool

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    chat_id: str
    chat_history: list[ChatMessage]

class ChatRequest(ChatResponse):
    question: str
