from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content":[
                { "type": "text", "text": "Generate two to three captions for this image in short" },
                { "type": "image_url", "image_url": {"url": "https://images.pexels.com/photos/36723948/pexels-photo-36723948.jpeg"} }
            ]
        }
    ]
)

print(f"🧠 : {response.choices[0].message.content}")