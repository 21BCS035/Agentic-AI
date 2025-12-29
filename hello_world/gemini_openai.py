from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key="AIzaSyDLZdx55vhm6BhRzjg10KuX6SQudjDSfVM",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"user","content":"Hey, I am Arpit Yadav! Nice to meet you"}
    ]
)

print(response.choices[0].message.content)