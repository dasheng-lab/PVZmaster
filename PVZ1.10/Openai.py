from openai import OpenAI
import re
import random

client = OpenAI(base_url="http://10.15.88.73:5012/v1", api_key="ollama")


def AI_talk(str):
    try:
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
    except:
        print("AI connection error")
        return "I don't know"


def AI_decision(str1, str2):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are the boss of zombie,you will get the coordinate of the enemy,and you can chose the y-coordinate of your zombie to attack the enemy or enter the house,which one will you chose?(from[425,315,230,125,25]) and you should answer it with only one number",
                },
                {
                    "role": "user",
                    "content": "answer me with only a number,if you are the boss of zombie,your enemy's coordinate is ("
                    + f"{str1}"
                    + ","
                    + f"{str2}"
                    + ") you can chose the y-coordinate of your zombie to attack the enemy or enter the house,which one will you chose?(from[425,315,230,125,25],please only reply a number)",
                },
            ],
            model="llama3.2",
        )
        return chat_completion.choices[0].message.content
    except:
        print("AI connection error")
        return f"{random.choice([425, 315, 210, 125, 25])}"
