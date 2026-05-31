import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai.errors import ClientError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set. Add it to your .env file or set it in the environment."
    )

client = genai.Client(api_key=api_key)

try:
    for model in client.models.list():
        print(model.name)
except ClientError as exc:
    print("Gemini API request failed:", exc)
    raise