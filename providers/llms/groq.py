from groq import Groq
from django.conf import settings

GROQ_API_KEY = settings.GROQ_API_KEY

class GroqService:
    def get_response(self, query, model):
        try:
            client = Groq(
            api_key=GROQ_API_KEY,
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": query    ,
                    }
                ],
                model=model,
            )

            return chat_completion
        except Exception as e:
            return {"error": str(e)}
    def parse_usage(self, query, response):
        try:
            usage = response.usage
            return {
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }
        except Exception as e:
            return {"error": str(e)}
    def get_content(self, response):
        try:
            return response.choices[0].message.content
        except Exception as e:
            return {"error": str(e)}
    
    
def groq_response(query):
    try:
        client = Groq(
            api_key=GROQ_API_KEY,
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": query    ,
                }
            ],
            model="groq/compound",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}
