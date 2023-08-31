import openai
from ai_platform.models import AIPlatform

openai.api_key = "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"


async def createChat(messages):
    return await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
