import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai.errors import ClientError

load_dotenv()

def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set in the environment. Set it in .env or your shell before running the app.")
    return genai.client.Client(api_key=api_key)


def get_answer(question, vector_store):

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    if not docs:
        raise ValueError("No relevant text was found in the uploaded PDF.")

    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
    Answer only using the provided context.

    Context:
    {context}

    Question:
    {question}
    """

    client = _get_client()
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
    except ClientError as exc:
        raise RuntimeError(
            "Gemini API request failed. Check GEMINI_API_KEY, model name, and network access."
        ) from exc

    return response.text