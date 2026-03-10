import replicate
from django.conf import settings

REPLICATE_API_KEY = settings.REPLICATE_API_KEY

class ReplicateService:    
     def get_response(self, query, model):
        try:
            # Set the API token as an environment variable for replicate library
            client = replicate.Client(api_token=REPLICATE_API_KEY)
            output = client.run(
                model,
                input={"prompt": query}
            )
            return output
        except Exception as e:
            return {"error": str(e)}

def replicate_response(query):
    try:
        # Set the API token as an environment variable for replicate library
        client = replicate.Client(api_token=REPLICATE_API_KEY)
        output = client.run(
            "mistralai/mistral-7b-instruct-v0.2",
            input={"prompt": query}
        )
        return output
    except Exception as e:
        return {"error": str(e)}
