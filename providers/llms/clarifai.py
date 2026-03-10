from clarifai import client
from clarifai.client import Model
from django.conf import settings

CLARIFAI_PAT = settings.CLARIFAI_PAT  # Personal Access Token

class ClarifaiClient:
    def get_response(self, query, model):
        try:
            client = Model(url=model, pat=CLARIFAI_PAT)
            response = client.predict(prompt="""Generate the response in clean human-readable text.
Formatting rules:
- No escape characters like \n or \t
- No JSON
- No quotes around the text
- Just plain paragraphs and bullet points if needed

Answer: """+ query)
            return response
        except Exception as e:
            return {"error": str(e)}
    def get_content(self, response):
        return response 
    def parse_usage(self, query, response):
        return {
            "input_tokens": len(query),
            "output_tokens": len(response),
            "total_tokens": len(query) + len(response),
        }   