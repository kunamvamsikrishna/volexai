from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from chat.models import Request ,Message , ChatSession
from rest_framework.response import Response
from authentication.authentication import APIkeyAuthentication
from .services import get_adapter, route_model, calculate_cost
from .models import LLms, Providers
from .seralizers import LLmSerializer, ProvidersSerializer
from django.db import transaction

class LLmCall(APIView):
    authentication_classes = [APIkeyAuthentication]
    def post(self,request):
        
        query = request.data.get('query')
        model = request.data.get('model')
        provider = request.data.get('provider')
        session_id = request.data.get('session_id')
        request_type = request.data.get('request_type',"apicall")

        if not query:
            return Response({"message": "Query is required"}, status=400)
        if not model:
            return Response({"message": "Model is required"}, status=400)
        if not provider:
            return Response({"message": "Provider is required"}, status=400)
        
        wallet = request.user.wallet
        if wallet.credits <= 0:
            return Response({"message": "Insufficient balance"}, status=400)
        
        try:
            model_obj  = route_model(model)
        except Exception  as e :
            return Response({"message": "Invalid model"}, status=400)
        
        chat_session = None
        if request_type == 'chat':
            if session_id:
                 chat_session = ChatSession.objects.filter(id=session_id, user=request.user).first()
            if not chat_session:
                chat_session = ChatSession.objects.create(user=request.user,title="New Chat",model=model_obj)    

        try:
            adapter =get_adapter(provider)
            store_request = Request.objects.create(
                    user=request.user,
                    model=model_obj,   
                    status='pending',
                    chat_session = chat_session,
                    request_type=request_type,
                    api_key = request.auth,
                    total_cost = 0
                )
            input_message = Message.objects.create(role="user", content=query, request=store_request ,chat_session= chat_session,user=request.user)

            response = adapter.get_response(query, model)
            message = adapter.get_content(response)
            usage = adapter.parse_usage(query,response) 
            cost = calculate_cost(model_obj, usage['input_tokens'], usage['output_tokens'])  

            if wallet.credits < cost['total_cost']:
                store_request.status = 'failed'
                store_request.save()
                return Response({"message": "Insufficient balance"}, status=400)
            
            with transaction.atomic():
                wallet.credits -= cost['total_cost']    
                wallet.save()
                output_message = Message.objects.create(role="assistant", content=message, request=store_request, token_count=usage['output_tokens'], chat_session= chat_session,user=request.user)
                input_message.token_count = usage['input_tokens']
                input_message.save()
                store_request.input_tokens = usage['input_tokens']
                store_request.output_tokens = usage['output_tokens']
                store_request.total_cost = cost['total_cost']
                store_request.status = 'completed'
                store_request.save()

            response_data = {
                    "message": message,
                    "usage": usage,
                    "cost": cost,
                    "model": model,
                    "provider": provider,
                    "session_id": chat_session.id if chat_session else None,
                 }
            return Response({"response": response_data}) 
        except Exception as e:
            store_request.status = 'failed'
            store_request.save()
            return Response({"error": str(e)}, status=500)
       
        


class SupportedModels(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        models = LLms.objects.all() 
        seralizer = LLmSerializer(models, many=True)
        return Response({"models": seralizer.data})




class ProvdersList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        providers = Providers.objects.all()
        seralizer = ProvidersSerializer(providers, many=True)
        return Response({"providers": seralizer.data})

































        # if model == 'gemini':
        #     response = gemini_response(query)
        #     return Response({"response": response})
        # if model == 'groq':
        #     response = groq_response(query)
        #     return Response({"response": response})
        # if model == 'openrouter':
        #     response = openrouter_response(query)
        #     return Response({"response": response})
        # if model == 'clarifai':
        #     response = clarifai_response(query)
        #     return Response({"response": response})
        # if model == "qubrid":
        #     response = qubrid_response(query)
        #     return Response({"response": response})
        # if model == "togetherai":
        #     response = together_response(query)
        #     return Response({"response": response})
        # if model == "replicate":
        #     response = replicate_response(query)
        #     return Response({"response": response})
        # if model == "fireworks":
        #     response = fireworks_response(query)
        #     return Response({"response": response})
        # if model == "claude":
        #     response = claude_response(query)
        #     return Response({"response": response})
        # if model == "openai":
        #     response = openai_response(query)
        #     return Response({"response": response})
        return Response({"message": "Model not supported"}, status=400)