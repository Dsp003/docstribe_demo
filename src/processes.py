from bson import ObjectId
from fastapi import HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import logging
import time

from src.db import (
    patient_collection,
    chat_collection
)
from src.prompts import create_system_message
from src.models import (
    BotResponse,
    Chat,
    ChatMessage,
    ChatResponse,
    ChatRequest
)
from src.helpers.openai_helper import get_bot_response

def dict_id_convertion(doc: dict):
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            doc[k] = str(v)

async def does_patient_exist(patient_id: str) -> bool:
    res = await patient_collection.find_one(
        {"_id": ObjectId(patient_id)},
        {"_id": 1}
    )
    return res != None

async def get_medical_history(patient_id: str) -> dict|None:
    res: dict = await patient_collection.find_one(
        {"_id": ObjectId(patient_id)},
        {"medical_history": 1}
    )
    if not res:
        return None
    history: dict = res.get("medical_history", dict())
    for val in history.values():
        if len(val) > 0:
            return history
    return None

async def is_medical_history_upload_pending(patient_id: str) -> bool:
    res = await chat_collection.find_one(
        {"patient_id": ObjectId(patient_id), "scenario": "review medical history", "action": "medical history upload", "status": "pending"},
        {"_id": 1}
    )
    return res != None

async def get_previous_medical_history_review(patient_id: str) -> list:
    cursor = chat_collection.find(
        {"patient_id": ObjectId(patient_id), "scenario": "review medical history", "action": "patient educated", "status": "pending"},
        {"_id": 1, "messages": 1}
    ).sort({"last_modified": -1}).limit(1)
    chat = list()
    async for doc in cursor:
        dict_id_convertion(doc)
        chat.append(doc)
    return chat

async def get_patient_chats_process(patient_id: str):
    if not await does_patient_exist(patient_id):
        raise HTTPException(status_code=404, detail="patient id not found")
    
    if await get_medical_history(patient_id):
        last_pending_chat = await get_previous_medical_history_review(patient_id)
        content = list()
        if len(last_pending_chat) == 1:
            last_pending_chat = last_pending_chat[0]
            content = {
                "chat_id": last_pending_chat["_id"],
                "chat_history": last_pending_chat["messages"]
            }
        response = jsonable_encoder({
            "type": "chat_history",
            "content": content
        })
        return JSONResponse(response)
    
    if await is_medical_history_upload_pending(patient_id):
        return JSONResponse({
            "type": "message",
            "content": [{
                "role": "assistant",
                "content": "Your medical history upload is being processed. Please try after some time or reach out to abcd@efg.com for updates."
            }]
        })
    
    return JSONResponse({
        "type": "message",
        "content": [{
            "role": "assistant",
            "content": "We don't have your medical history. Please reach out to abcd@efg.com for uploading your medical history."
        }]
    })

async def create_chat_process(patient_id: str):
    medical_history = await get_medical_history(patient_id)
    if not medical_history:
        raise HTTPException(status_code=400, detail="no medical history found for the given patient id")
    
    system_message = create_system_message(medical_history)

    # try:
    res = await chat_collection.insert_one(
        {
            "scenario": "review medical history",
            "action": "patient educated",
            "status": "pending",
            "patient_id": ObjectId(patient_id),
            "last_modified": time.time(),
            "messages": [
                {"role": "system", "content": system_message}
            ]
        }
    )
    response = ChatResponse(
        chat_id=str(res.inserted_id),
        chat_history=[
            ChatMessage(
                role="system",
                content=system_message
            )
        ]
    )
    response = response.model_dump()
    return JSONResponse(jsonable_encoder(response), status_code=201)
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=500, detail="An error occured. Try after some time.")
    
async def chat_process(request: ChatRequest):
    request.chat_history.append(
        ChatMessage(
            role="user",
            content=request.question
        )
    )
    try:
        bot_response: BotResponse = await get_bot_response(
            messages=request.model_dump()["chat_history"],
            response_model=BotResponse,
        )
        request.chat_history.append(
            ChatMessage(
                role="assistant",
                content=bot_response.content
            )
        )
        await chat_collection.update_one(
            filter={"_id": ObjectId(request.chat_id)},
            update={
                "$set": {
                    "messages": request.model_dump()["chat_history"],
                    "status": "done" if bot_response.is_over else "pending",
                    "last_modified": time.time()
                }
            }
        )
        return JSONResponse(jsonable_encoder(request.model_dump()))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occured. Try after some time.")