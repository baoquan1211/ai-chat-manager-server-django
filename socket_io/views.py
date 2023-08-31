import os
import socketio

from services.openai.views import createChat as openai_chat
from services.palm.views import createChat as palm_chat
from conversation.models import Conversation
from user.models import User
import json
from .message_filter import message_filter

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
                # questions=json.dumps(questions),
            )
            conversation.save()
        else:
            conversation = Conversation.objects.get(id=data.get("conversation"))
            messages = json.loads(conversation.messages)

            # questions = json.loads(conversation.questions)

        # questions.append(data["message"])
        blocked_words = await message_filter(data["message"]["content"])

        if len(blocked_words) > 0:
            response = {
                "role": "server",
                "content": "Your message was blocked as It contains some blocked words. Please try again.",
                "blocked": True,
            }
        else:
            ai_platform = data.get("ai_platform", "openai")
            if ai_platform == "openai":
                prompt = []
                for message in messages:
                    if message["role"] == "user":
                        prompt.append(message)
                    else:
                        prompt.append(
                            {"role": "assistant", "content": message["content"]}
                        )
                messages.append(data["message"])
                prompt.append(data["message"])
                response = await openai_chat(messages=prompt)
                response = list(response.choices)[0]
                response = response.to_dict()["message"]["content"]
                response = {"role": "openai", "content": response}

            else:
                messages.append(data["message"])
                prompt = []
                for message in messages:
                    prompt.append(message["content"])
                response = await palm_chat(messages=prompt)
                print(response)
                if response == None:
                    response = "Sorry, I can't understand your request."
                response = {"role": "palm", "content": response}

        package = {
            "conversation": conversation.id,
            "response": response,
        }

        messages.append(response)
        conversation.messages = json.dumps(messages)
        # conversation.questions = json.dumps(questions)
        conversation.save()

        await sio.emit("answer_request", package)
        print("server" ": replied successfully")
    except:
        await sio.emit(
            "answer_request",
            {"error": "Something went wrong", conversation: data.get("conversation")},
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
