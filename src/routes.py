from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db import init_db, close_db
from src.models import ChatRequest
from src.processes import (
    chat_process,
    get_patient_chats_process, 
    create_chat_process
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() 
    yield
    close_db()

app = FastAPI(lifespan=lifespan)


@app.get("/chat/patient/{patient_id}")
async def get_patient_chats(patient_id: str):
    return await get_patient_chats_process(patient_id)

@app.post("/chat")
async def create_chat(patient_id: str):
    return await create_chat_process(patient_id)

@app.put("/chat")
async def chat(request: ChatRequest):
    return await chat_process(request)