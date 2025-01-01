import os
from openai import AsyncOpenAI

# from src.models import (
#     BotResponse,
#     Chat,
#     ChatMessage,
#     ChatRequest
# )

openai_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_KEY")
)

OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")

async def get_bot_response(messages: list, response_model, temperature: float=0.3, max_tokens: int=200):
    response = await openai_client.beta.chat.completions.parse(
        model=OPENAI_CHAT_MODEL,
        messages=messages,
        response_format=response_model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.parsed