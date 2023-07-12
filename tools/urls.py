from django.urls import path
from .views import (
    tools_main_view, 
    chatbot_general, 
    chatbot_translation, 
    generate_image_from_txt, 
    get_response_for_general,
    get_response_for_translation,
    get_response_for_image,
)

app_name = 'tools'

urlpatterns = [
    path('', tools_main_view, name='main'),
    path('openai/general/', chatbot_general, name='openai-general'),
    path('openai/translation/', chatbot_translation, name='openai-translation'),
    path('openai/image/', generate_image_from_txt, name='openai-image'),
    path('openai/get-general/', get_response_for_general, name='openai-get-general'),
    path('openai/get-translation/', get_response_for_translation, name='openai-get-translation'),
    path('openai/get-image/', get_response_for_image, name='openai-get-image'),
]