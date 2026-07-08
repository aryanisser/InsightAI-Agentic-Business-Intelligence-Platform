import os
from dotenv import load_dotenv
from openai import OpenAI
from config import MODEL_NAME

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def ask_business_data(context, question):
    prompt = f"""
You are an expert Business Intelligence Consultant.

Dataset Context:
{context}

Question:
{question}

Answer professionally with insights and recommendations.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI service error: {e}"