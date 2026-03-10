import os 
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / '.env')
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

class FireworksService:
    def get_response(self, query, model):
        try:
            url = "https://api.fireworks.ai/inference/v1/chat/completions"
            payload = {
            "model": f"accounts/fireworks/models/{model}",
            # "max_tokens": 25344,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.6,
            "messages": [
                {
                "role": "user",
                "content": query
                }
            ]
            }
            headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {FIREWORKS_API_KEY}"
            }
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    def get_content(self, response):
        try:
            return response['choices'][0]['message']['content']
        except Exception as e:
            return {"error": str(e)}
    def parse_usage(self, query, response):
        try:
            usage = response.get('usage', {})
            return {
                "input_tokens": usage.get('prompt_tokens', 0),
                "output_tokens": usage.get('completion_tokens', 0),
                "total_tokens": usage.get('total_tokens', 0),
            }
        except Exception as e:
            return {"error": str(e)}

