import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

for model in client.models.list():
    print("=" * 50)
    print("NAME:", model.name)

    if hasattr(model, "supported_actions"):
        print("SUPPORTED:", model.supported_actions)

    if hasattr(model, "supported_generation_methods"):
        print("METHODS:", model.supported_generation_methods)