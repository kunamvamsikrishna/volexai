from django.urls import path
from providers.views import LLmCall, ProvdersList, SupportedModels


urlpatterns = [
    path('llm/', LLmCall.as_view(), name='llm'),
    path('models/', SupportedModels.as_view(), name='supported_models'),
    path('providers/', ProvdersList.as_view(), name='providers_list'),
]