from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/main.html', context)



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profiles:my')