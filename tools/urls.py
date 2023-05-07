from django.urls import path
from .views import ToolsMain

app_name = 'tools'

urlpatterns = [
    path('', ToolsMain, name='main'),
]