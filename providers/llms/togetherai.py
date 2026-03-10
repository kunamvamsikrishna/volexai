from together import Together
from django.conf import settings

TOGETHERAI_API_KEY = settings.TOGETHERAI_API_KEY

class TogetherAIService:
    def get_response(self, query, model):
        try:
            import requests

            url = "https://api.together.xyz/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {TOGETHERAI_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": query}
                ],
                "max_tokens": 200
            }

            response = requests.post(url, headers=headers, json=data)
            return response
        except Exception as e:
            return {"error": str(e)}

def together_response(query):
    try:
        import requests

        url = "https://api.together.xyz/v1/chat/completions"

        headers = {
            "Authorization": "Bearer key_CYiVhJs9zRMaA2DmNwBtx",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {"role": "user", "content": query}
            ],
            "max_tokens": 200
        }

        response = requests.post(url, headers=headers, json=data)

        return response
    except Exception as e:
        return {"error": str(e)}
    