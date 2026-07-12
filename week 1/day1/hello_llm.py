import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"
prompt = "Write a python script that prints 'Hello, World!'"

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)