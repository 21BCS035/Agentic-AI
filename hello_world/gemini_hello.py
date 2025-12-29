from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hi! My name is Arpit Yadav Nice to meet you",
)

print(response.text)