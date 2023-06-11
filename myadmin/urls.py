from django.urls import path
from myadmin.views import MemberList, MemberDetails, member_list_view, member_detail_view, member_add_view, member_delete_view

app_name = 'myadmin'

urlpatterns = [
#    path('', MemberList.as_view(), name='memberlist'),
#    path('<int:page>', MemberList.as_view(), name='memberlist'),
#    path('details/<pk>', MemberDetails.as_view(), name='memberdetails'),
    path('', member_list_view, name='memberlist'),
    path('<int:page>', member_list_view, name='memberlist'),
    path('details/<int:pk>', member_detail_view, name='memberdetails'),
    path('add/', member_add_view, name="member-add"),
    path('<int:pk>/delete/', member_delete_view, name="member-delete"),
]