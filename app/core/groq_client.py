import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # 👈 THIS IS REQUIRED

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)