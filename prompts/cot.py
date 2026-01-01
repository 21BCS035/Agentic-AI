#Chain of thought prompting

import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT="""
   You're an expert AI assistant in resloving user queries using chain of thought.
   You work on START, PLAN and OUTPUT steps.
   You need to first PLAN what needs to be done. The plan can be multiple steps.
   Once you think enough PLAN has been done, finally you can give an OUTPUT.

   RULES:
   - Strictly Follow the given JSON output format
   - Only run one step at a time
   - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

   Output JSON format:
   { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

   Example:
   START: Hey, can you solve 2 + 3 * 5 / 10
   PLAN: { "step": "PLAN": "content": "Seems like user is asking about a math problem" }
   PLAN: { "step": "PLAN": "content": "looking at the problem, we can solve this using BODMAS method" }
   PLAN: { "step": "PLAN": "content": "Yes, the BODMAS is correct method to be done here" }
   PLAN: { "step": "PLAN": "content": "first we should multiply 3 * 5 which is 15" }
   PLAN: { "step": "PLAN": "content": "Now the new eqation is 2 + 15 / 10" }
   PLAN: { "step": "PLAN": "content": "we must perform divide operation that is 15 / 10 = 1.5" }
   PLAN: { "step": "PLAN": "content": "Now the new eqation is 2 + 1.5" }
   PLAN: { "step": "PLAN": "content": "Now finally lets perform the add operation which becomes 3.5" }
   PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as answer" }
   OUTPUT: { "step": "OUTPUT": "content": "3.5" }
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_query = input("👍 ")
message_history.append({ "role": "user", "content": user_query })

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥 ",parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "PLAN":
        print("🧠 ",parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🏢 ",parsed_result.get("content"))
        break


print("\n\n\n")
# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     messages=[
#         {"role":"system","content":SYSTEM_PROMPT},
#         {"role":"user","content":"Hey,Write a code in python for adding two numbers"}
#     ]
# )


# print(response.choices[0].message.content)