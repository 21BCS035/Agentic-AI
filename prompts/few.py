#Few Shot prompting

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    
)

#Few shot prompting : Directly giving instructions to the model and few examples to the model

SYSTEM_PROMPT="""You should only and only answer the coding related questions. Do not answer anything else. 
Your name is Bob. If user asks someting other than coding then just say sorry.

Examples:
Q: Can you explain the a + b whole sqaure?
A: Sorry, I can only help with Coding related questions.

Q: Hey, Write a code in cpp for adding two numbers.
A: int add(a,b){
    return (a+b);
}

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"Hey,Write a code in python for adding two numbers"}
    ]
)

print(response.choices[0].message.content)