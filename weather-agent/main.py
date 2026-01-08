#Chain of thought prompting

import json
from openai import OpenAI
from dotenv import load_dotenv
import requests
from pydantic import BaseModel,Field
from typing import Optional
import os

load_dotenv()

client = OpenAI()

session = requests.Session()

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    headers = {
        "User-Agent": "curl/8.0",    
        "Connection": "close"        
    }

    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return f"The weather in {city} is {response.text}"

def run_command(cmd: str):
    result = os.system(cmd)
    return result

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT="""
   You're an expert AI assistant in resloving user queries using chain of thought.
   You work on START, PLAN and OUTPUT steps.
   You need to first PLAN what needs to be done. The plan can be multiple steps.
   Once you think enough PLAN has been done, finally you can give an OUTPUT.
   You can also call a tool if required from the list of available tools.
   For every tool call wait for the observe step which is the output from the called tool.

   RULES:
   - Strictly Follow the given JSON output format
   - Only run one step at a time
   - The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

   Output JSON format:
   { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string","input":"string" }

   Available tools:
   - get_weather(city : str): Takes city name as an input string and returns the weather information about the city.
   - run_command(cmd : str): Takes a system linux command as string and executes the command on user's system and returns the output from that command.

   Example 1:
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

   Example 2:
   START: What is the weather of Bangalore?
   PLAN: { "step": "PLAN": "content": "Seems like user is interested in knowing the weather of Bangalore" }
   PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of avaiable tools" }
   PLAN: { "step": "PLAN": "content": "Great! we have get_weather tool available for this query" }
   PLAN: { "step": "TOOL": "tool": "get_weather", "input": "Bangalore" }
   PLAN: { "step": "OBSERVE": "tool": "get_weather", "output":"The Temperature of Bangalore is 24 C" }
   PLAN: { "step": "PLAN": "content": "Great, I got the weather information of Bangalore" }
   OUTPUT: { "step": "OUTPUT": "content": "The current weather of Bangalore is 24 C with some cloudy sky" }
"""

class OutputFormat(BaseModel):
    step: str = Field(...,description="The ID of the step.Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None,description="The optional string content for the step.")
    input: Optional[str] = Field(None,description="The input params for the tool.")
    tool: Optional[str] = Field(None,description="The ID of the tool to call.")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


while True:
    user_query = input("👍 ")
    message_history.append({ "role": "user", "content": user_query })
    if user_query in ["bye", "exit", "quit", "q"]:
        print("bye👋")
        break


    while True:
        response = client.chat.completions.parse(
            model="gpt-4o-mini",
            response_format=OutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role":"assistant","content":raw_result})
        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("🔥 ",parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🧰: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🧰: {tool_to_call} ({tool_input} = {tool_response})")
            message_history.append({"role":"developer","content":json.dumps(
                {"step":"OBSERVE","tool":tool_to_call,"input":tool_input,"output":tool_response}
            )})
            continue

            
        
        if parsed_result.step == "PLAN":
            print("🧠 ",parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🏢 ",parsed_result.content)
            break
