import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

message_system = {
    "role": "system",
    #"content": "You are my senior manager , she is very strict and professional , disciplined." #this is for system 
    "content": "you are a brand manager who suggest me food companies. name s" #this is for system
}

message = {
    "role": "user",
    "content": "Suggest me a food name for my company ." #this is for user
}

response = client.chat.completions.create(
    model=model,
    messages=[message_system, message],
    temperature=1,
)

print(response.choices[0].message.content)