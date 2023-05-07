from django.urls import path
from profiles.views import MemberList, MemberDetails
from .views import myAdmin

app_name = 'myadmin'

urlpatterns = [
    path('', MemberList, name='memberlist'),
    path('<int:page>', MemberList, name='memberlist'),
    path('details/<pk>', MemberDetails, name='memberdetails'),
]