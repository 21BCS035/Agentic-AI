from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"user","content":"Hey, I am Arpit Yadav! Nice to meet you"}
    ]
)

print(response.choices[0].message.content)