from huggingface_hub import InferenceClient
from django.conf import settings

HUGGINGFACE_API_KEY = settings.HUGGINGFACE_API_KEY

class HuggingFaceService:
    def get_response(self, query, model):
        try:
            client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

            # output is a PIL.Image object
            completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ],
        )

            return completion
        except Exception as e:
            return {"error": str(e)}
    def parse_usage(self,query,response):
        try:
            usage = response.usage
            return {
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }
        except Exception as e:
            return {"error": str(e)}
    def get_content(self,response):
        try:
            return response.choices[0].message.content
        except Exception as e:
            return {"error": str(e)}

    


# model = "katanemo/Arch-Router-1.5B"