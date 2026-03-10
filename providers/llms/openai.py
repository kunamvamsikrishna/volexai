from openai import OpenAI
from django.conf import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAIService:
    def get_response(self, query, model):   
        try:
            response = client.responses.create(
                model=model,
                input=query
            )
            return response.output_text
        except Exception as e:
            return {"error": str(e)}
