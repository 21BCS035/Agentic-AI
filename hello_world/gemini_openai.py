from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
#    api key is going to be written here
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":"You are an expert in Computer Science and programming,so give the answers related to thsese things only"},
        {"role":"user","content":"Write a code in cpp to print sum of two numbers"}
    ]
)

print(response.choices[0].message.content)