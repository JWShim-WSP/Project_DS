from django.urls import path
from .views import tools_main_view, chatbot_general, chatbot_translation, generate_image_from_txt


app_name = 'tools'

urlpatterns = [
    path('', tools_main_view, name='main'),
    path('openai/general/', chatbot_general, name='openai-general'),
    path('openai/translation/', chatbot_translation, name='openai-translation'),
    path('openai/image/', generate_image_from_txt, name='openai-image'),
]