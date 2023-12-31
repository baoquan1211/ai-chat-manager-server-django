import os
import socketio
from conversation.models import Conversation
from user.models import User
import json
from .message_filter import message_filter
from asgiref.sync import sync_to_async
from ai_platform.views import OpenAI, PaLM

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    ping_timeout=1000 * 60,
    async_mode="asgi",
    reconnection=True,
)
app = socketio.ASGIApp(sio)


@sio.event
async def ask_request(sid, data):
    print(data.get("user", "undefined"), ": ", data["message"]["content"])
    messages = []

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
            )
            conversation.save()
        else:
            conversation = Conversation.objects.get(id=data.get("conversation"))
            messages = json.loads(conversation.messages)
        blocked_words = await message_filter(data["message"]["content"])

        if len(blocked_words) > 0:
            response = {
                "role": "server",
                "content": "Your message was blocked as It contains some blocked words. Please try again.",
                "blocked": True,
            }
        else:
            ai_platform = data.get("ai_platform", "openai")
            messages.append(data["message"])
            if ai_platform == "openai":
                ai_platform = OpenAI()
                response = await ai_platform.get_answer(messages)

            elif ai_platform == "palm":
                ai_platform = PaLM()
                response = await ai_platform.get_answer(messages)

        package = {
            "conversation": conversation.id,
            "response": response,
        }

        messages.append(response)
        conversation.messages = json.dumps(messages)
        conversation.save()

        await sio.emit("answer_request", package)
        print("server" ": replied successfully")
    except Exception as e:
        print("error", e)
        await sio.emit(
            "answer_request",
            {"error": "Something went wrong", "conversation": data.get("conversation")},
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
