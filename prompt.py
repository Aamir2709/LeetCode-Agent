import requests
import os

def get_hint_from_huggingface(problem_title, problem_description):
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    hf_token = os.getenv("HF_TOKEN") 

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Problem Title: {problem_title}\n\n"
        f"Problem Description:\n{problem_description[:5000]}...\n\n"
        f"Please provide a motivational message and a useful hint to solve the above problem."
    )
    print("Prompt for Hugging Face API:", prompt)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        output = response.json()
        return output[0]["generated_text"]
    else:
        print("Error:", response.status_code, response.text)
        return None


