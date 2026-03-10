from google import genai
from django.conf import settings

class GeminiService:
    def get_response(self, query, model):
        GEMINI_API_KEY = settings.GEMINI_API_KEY
        client = genai.Client(api_key=GEMINI_API_KEY)
        try:
            response = client.models.generate_content(
                model=model,
                contents=query,
            )
            return response
        except Exception as e:
            return {"error": str(e)}


    def parse_usage(self, query,response):
        try:
            usage = response.usage_metadata
            return {
                 "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count
               
            }
            
        except Exception as e:
            return {"error": str(e)}    


    def get_content(self, response):
        try:
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            return {"error": str(e)}


