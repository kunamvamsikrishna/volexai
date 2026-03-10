import anthropic
from django.conf import settings

CLAUDE_API_KEY = settings.CLAUDE_API_KEY

class ClaudeService:     
        def get_response(self, query, model):
            try:
                client = anthropic.Client(api_key=CLAUDE_API_KEY)
                response = client.messages.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                )
                return response
            except Exception as e:
                return {"error": str(e)}