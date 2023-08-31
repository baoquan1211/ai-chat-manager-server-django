# txt = "  hello, my name is Peter, \nI am 26 years old "
# x = txt.split()
# print(x)
# new_x = []
# for i in x:
#     i = i.replace(",", "")
#     i = i.replace(".", "")
#     new_x.append(i)
# print(new_x)


import pprint
import google.generativeai as palm

palm.configure(api_key="AIzaSyCsNq2yyn9z561kOxQ5BUbI6XnK7BBOyNU")

models = [m for m in palm.list_models()]
# # model = models[0].name
print(models)

# prompt = [
#     {"message": "how to call api in python"},
#     {"message": "how about java"},
#     {"message": "how about flutter"},
# ]
# prompt = [
#     {"role": "user", "content": "hello", "platform": "openai"},
#     {"role": "user", "content": "how to learn nestjs", "platform": "openai"},
# ]
# messages = []
# for message in prompt:
#     # item = {"author": "0", "content": message["content"]}
#     messages.append(message["content"])


# async def chat(messages):
#     completion = await palm.chat_async(
#         model="models/chat-bison-001",
#         messages=messages,
#         temperature=0,
#         # The maximum length of the response
#         # max_output_tokens=800,
#     )
#     print(completion.last)


# chat(messages)

# import openai

# from chat_provider.models import ChatProvider

# openai.api_key = "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"

# messages = []
# for item in prompt:
#     temp = item
#     del temp["platform"]
#     messages.append(temp)
# chat = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=messages,
#     temperature=0.2,
# )

# print(chat)
