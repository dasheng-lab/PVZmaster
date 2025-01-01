from openai import OpenAI
import re

client=OpenAI(
    base_url='http://10.15.88.73:5012/v1',
    api_key='ollama'
)
def AI_talk(str):
    chat_completion=client.chat.completions.create(
        messages=[
            {"role":"system",
            "content":"you are a assistant"},
            {"role":"user",
            "content":str}
        ],
        model="llama3.2"
    )
    chat_completion0=re.split(r'[,.?!]',chat_completion.choices[0].message.content)
    return chat_completion0
def AI_decision(str1,str2):
    chat_completion=client.chat.completions.create(
        messages=[
            {"role":"system",
            "content":"you are a assistant"},
            {"role":"user",
            "content":"answer me with only a number,if you are the boss of zombie,your enemy's coordinate is ("+f"{str1}"+','+f"{str2}"+") you can chose the y-coordinate of your zombie to attack the enemy or enter the house,which one will you chose?(from[425,315,230,125,25])"}
        ],
        model="llama3.2"
    )
    return chat_completion.choices[0].message.content