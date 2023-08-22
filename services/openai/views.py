import os
import openai

openai.api_key = "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"

""" response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "hello"}],
    temperature=0.2,
) """


async def createChat(messages):
    return await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
