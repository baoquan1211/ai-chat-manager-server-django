import os
import openai

openai.api_key = "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"


async def createChat(messages):
    return await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
