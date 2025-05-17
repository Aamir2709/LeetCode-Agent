import requests
import os
from groq import Groq


def get_hint_from_groq(problem_title, problem_description):
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    prompt = (
        f"Problem Title: {problem_title}\n\n"
        f"Problem Description:\n{problem_description[:5000]}...\n\n"
        f"Please provide a motivational message and a useful hint to solve the above problem."
    )
    response = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
        top_p=0.95,
    )

    return response.choices[0].message.content.strip()
