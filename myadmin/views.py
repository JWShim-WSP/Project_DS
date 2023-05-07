from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from profiles.views import MemberList
from django.urls import reverse



# Create your views here.

@staff_member_required
def myAdmin(request):
    pass