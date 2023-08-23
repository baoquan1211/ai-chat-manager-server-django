import os
import socketio
from services.openai.views import createChat
from conversation.models import Conversation
from django.contrib.auth.models import User
import json
import re
from words_filter.models import WordsFilter
from asgiref.sync import sync_to_async

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    ping_timeout=1000 * 60,
    async_mode="asgi",
    reconnection=True,
)
app = socketio.ASGIApp(sio)


async def message_filter(message):
    blocked_words = []
    lower_message = message.lower()
    splited_message = lower_message.split()
    list_word_of_message = []
    for word in splited_message:
        word = word.replace(",", "")
        word = word.replace(".", "")
        list_word_of_message.append(word)

    blocked_words = WordsFilter.objects.get()
    blocked_words = json.loads(blocked_words.key_words)

    founded_words = []
    for word in blocked_words:
        if word in list_word_of_message:
            founded_words.append(word)
    return founded_words


@sio.event
async def ask_request(sid, data):
    print(data.get("user", "undefined"), ": ", data["message"]["content"])
    messages = []
    questions = []
    if data.get("user") is None:
        await sio.emit("answer_request", "User not found")
        return
    user = User.objects.get(username=data["user"])
    try:
        if data.get("conversation") is None:
            conversation = Conversation(
                name=data["message"]["content"],
                user_id=user,
                provider_id=1,
                messages=json.dumps(messages),
                questions=json.dumps(questions),
            )
            conversation.save()
        else:
            conversation = Conversation.objects.get(id=data.get("conversation"))
            messages = json.loads(conversation.messages)
            questions = json.loads(conversation.questions)

        messages.append(data["message"])
        questions.append(data["message"])
        blocked_words = await message_filter(data["message"]["content"])

        if len(blocked_words) > 0:
            response = {
                "role": "server",
                "content": "Your message was blocked as It contains some blocked words. Please try again.",
                "blocked": True,
            }
        else:
            response = await createChat(messages=questions)
            response = list(response.choices)[0]
            response = response.to_dict()["message"]

        package = (
            {
                "conversation": conversation.id,
                "response": response,
            },
        )
        messages.append(response)
        conversation.messages = json.dumps(messages)
        conversation.questions = json.dumps(questions)
        conversation.save()

        await sio.emit("answer_request", package)
        print("server" ": replied successfully")
    except Exception as error:
        await sio.emit(
            "answer_request",
            {error: str(error), conversation: data.get("conversation")},
        )


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, environ):
    print(sid, ": connected")
    # sio.emit("answer_request", sid)


@sio.event
def disconnect(sid):
    print(sid, ": disconnected")
