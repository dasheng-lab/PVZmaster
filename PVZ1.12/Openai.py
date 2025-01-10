from openai import OpenAI
import re
import random

client = OpenAI(base_url="http://10.15.88.73:5015/v1", api_key="ollama")


def AI_talk(str):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are an assistant and shopper of a game,if the player ask you a question,please answer it in a proper situtation",
            },
            {"role": "user", "content": str},
        ],
        model="llama3.2",
    )
    # chat_completion0 = re.split(r"[,.?!]", chat_completion.choices[0].message.content)
    return split_str(chat_completion.choices[0].message.content)


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


def comb_str(string_list):
    result = []
    current_string = ""
    punctuation = re.compile(r"[,.?!]")
    for s in string_list:
        if not current_string:
            current_string = s
        else:
            if s == "" or s == " " or s == "\n":
                continue
            else:
                if punctuation.search(s[-1]):
                    current_string += s
                    result.append(current_string)
                    current_string = ""
                else:
                    current_string += "" + s
    if current_string:
        result.append(current_string)
    return result


def split_str(input_string):
    result = []
    words = input_string.split()
    for i in range(0, len(words)):
        if len(words) == 0:
            break
        sentence = "" + words.pop(0)
        while len(sentence) < 65:
            if len(words) == 0:
                break
            sentence += " " + words.pop(0)
        result.append(sentence)
    return result
