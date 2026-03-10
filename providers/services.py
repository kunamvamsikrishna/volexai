from decimal import Decimal

from .models import LLms
from rest_framework.exceptions import ValidationError
from .llms.openai import OpenAIService
from .llms.clarifai import ClarifaiClient
from .llms.claude import ClaudeService
from .llms.fireworks import FireworksService
from .llms.gemini import GeminiService
from .llms.groq import GroqService
from .llms.togetherai import TogetherAIService
from .llms.openrouter import OpenRouterService
from .llms.qubrid import QubridService
from .llms.huggingface import HuggingFaceService
from .llms.replicate import ReplicateService 



def route_model(model_name):
    model = LLms.objects.filter(name=model_name).first()
    if not model:
        raise ValidationError("Requested model is not available")
    return model

def get_adapter(model_name):
     adapters = {
        "clarifai": ClarifaiClient,
        "openai": OpenAIService,
        "anthropic": ClaudeService,
        "gemini": GeminiService,
        "groq": GroqService,
        "togetherai": TogetherAIService,
        "openrouter": OpenRouterService,
        "qubrid": QubridService,
        "replicate": ReplicateService,
        "fireworks": FireworksService,
        "huggingface": HuggingFaceService,
       }
     
     adapter_class = adapters.get(model_name.lower())

     if not adapter_class:
            raise ValidationError("No adapter found for the specified model")
     return adapter_class()

def calculate_cost(llm, input_tokens, output_tokens):
    input_cost = (Decimal(input_tokens) / Decimal(1_000_000)) * llm.input_token_cost
    output_cost = (Decimal(output_tokens) / Decimal(1_000_000)) * llm.output_token_cost
    total_cost = input_cost + output_cost
    return {
        "total_cost": total_cost
    }