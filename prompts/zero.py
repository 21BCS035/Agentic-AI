#Zero Shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    
)

#Zero shot prompting : Directly giving instructions to the model

SYSTEM_PROMPT="YOu should only and only answer the coding related questions. Do not answer anything else. Your name is Bob. If user asks someting other than coding then just say sorry."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"write a program in cpp(write logic only) to sort an array in descending order"}
    ]
)

print(response.choices[0].message.content)