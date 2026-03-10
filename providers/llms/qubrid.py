from openai import OpenAI
from django.conf import settings

QUBRID_API_KEY = settings.QUBRID_API_KEY


class QubridService:    
    def get_response(self, query, model):
        try:
            client = OpenAI(
            base_url="https://platform.qubrid.com/v1",
            api_key=QUBRID_API_KEY,
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                {
                    "role": "user",
                    "content": query
                }
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content  
        except Exception as e:
            return {"error": str(e)}  
    
    
def qubrid_response(query):
    try:
       client = OpenAI(
        base_url="https://platform.qubrid.com/v1",
        api_key=QUBRID_API_KEY,
        )

       response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
            {
                "role": "user",
                "content": query
            }
            ],
            max_tokens=500,
            temperature=0.7
        )

       return response.choices[0].message.content  
    except Exception as e:
        return {"error": str(e)}  
def parse_usage(query,response):
        usage = response.usage
        return {
            "input_tokens": usage.prompt_tokens,
            "output_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }
def get_content(response):
        try:
            return response.choices[0].message.content
        except Exception as e:
            return {"error": str(e)}