import openai
from chat_provider.models import ChatProvider

openai.api_key = ChatProvider.objects.get(name="OpenAI").key


async def createChat(messages):
    return await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )
