import google.generativeai as palm
from ai_platform.models import AIPlatform


palm.configure(api_key=AIPlatform.objects.get(name="PaLM").key)


async def createChat(messages):
    response = await palm.chat_async(
        model="models/chat-bison-001",
        messages=messages,
        temperature=0.2,
    )
    return response.last
