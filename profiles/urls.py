from django.urls import path
from .views import my_profile_view, ChangePasswordView

app_name = 'profiles'

urlpatterns = [
    path('', my_profile_view, name='my'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    #path('<str:format>/', views.Export, name='Export'),
]