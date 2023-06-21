from django.urls import path
from .views import tools_main_view


app_name = 'tools'

urlpatterns = [
    path('', tools_main_view, name='main'),
]