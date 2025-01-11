from openai import OpenAI
import re
import random

client = OpenAI(base_url="http://10.15.88.73:5012/v1", api_key="ollama")


def AI_talk(str):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are an assistant",  # "you are an assistant of a game,if the player ask you a question,please answer it in a proper situtation",
            },
            {"role": "user", "content": str},
        ],
        model="llama3.2",
    )
    # chat_completion0 = re.split(r"[,.?!]", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


print(AI_talk("hello"))
