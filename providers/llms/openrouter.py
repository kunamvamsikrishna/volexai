import requests
import json
from django.conf import settings

OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY
class OpenRouterService:
    def get_response(self, query, model):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                },
                data=json.dumps({
                    "model": model,
                    "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                    ]
                })
                )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    def get_content(self, response):
        try:
            return response['choices'][0]['message']['content']
        except Exception as e:
            return {"error": str(e)}
        
    def parse_usage(self,query,response):
           usage = response.get('usage', {})
           return {
                "input_tokens": usage.get('prompt_tokens', 0),
                "output_tokens": usage.get('completion_tokens', 0),
                "total_tokens": usage.get('total_tokens', 0),
              }