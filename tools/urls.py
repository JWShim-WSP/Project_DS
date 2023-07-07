from django.urls import path
from .views import tools_main_view, chatbot, generate_image_from_txt


app_name = 'tools'

urlpatterns = [
    path('', tools_main_view, name='main'),
    path('chatbot/', chatbot, name='chatbot'),
    path('davinci/', generate_image_from_txt, name='davinci'),
]