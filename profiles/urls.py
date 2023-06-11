from django.urls import path
from .views import (
    my_profile_view, 
    ChangePasswordView, 
    invites_received_view, 
    invite_profiles_list_view,
    FriendsListView,
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('myprofile/', my_profile_view, name='my'),
    path('to-invite/', invite_profiles_list_view, name='invite-profiles-view'),
    path('my-friends/', FriendsListView.as_view(), name='my-friends-view'),
    path('detail/<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('my-invites/accept/', accept_invitation, name='accept-invite'),
    path('my-invites/reject/', reject_invitation, name='reject-invite'),
    path('remove-friend/', remove_from_friends, name='remove-friend'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]