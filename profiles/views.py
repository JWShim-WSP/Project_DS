from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Relationship
from bulletin.models import Bulletin, Comment
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    number_of_likers = 0
    number_of_comments = 0
    number_of_replies = 0

    post_qs = Bulletin.objects.filter(poster=request.user.profile)
    number_of_posts = post_qs.count()

    for post in post_qs:
        number_of_likers += post.number_of_likers()
        number_of_comments += post.number_of_comments()
        comment_qs = Comment.objects.filter(CommentPost=post)
        for comment in comment_qs:
            number_of_children = comment.children.count()
            if (number_of_children):
                number_of_replies += number_of_children
                # if a comment has children, then it must be de-counted for children from the comment count
                number_of_comments -= number_of_children

    friends_list = profile.get_friends()
    number_of_friends = profile.get_friends_no()
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            profile = Profile.objects.get(user=request.user)
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
        'number_of_posts': number_of_posts,
        'number_of_likers': number_of_likers,
        'number_of_comments': number_of_comments,
        'number_of_replies': number_of_replies,
        'friends_list': friends_list,
        'number_of_friends': number_of_friends,
    }
    return render(request, 'profiles/main.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        posts = self.get_object().get_all_posters_posts()
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = posts
        context['len_posts'] = True if len(posts) > 0 else False
        return context

class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'profiles/friends_list.html'

    def get_queryset(self):
        qs = Profile.objects.get(user=self.request.user).friends.all()
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_receiver = []
        for item in rel_r:
            if item.status == 'send':
                rel_receiver.append(item.receiver)
        # all people who received my invitations and not accepted yet
        context["rel_receiver"] = rel_receiver
        if len(self.get_queryset()) == 0 and len(rel_receiver) == 0:
            context['is_empty'] = True
        return context


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profiles_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        # all people who received my invitations
        context["rel_receiver"] = rel_receiver
        # all people who sent invitations to me
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}
    context['is_empty'] = False
    if len(qs) == 0:
        context['is_empty'] = True

    return render(request, 'profiles/to_invite_list.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }
    return render(request, 'profiles/my_invites.html', context)

def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my')

def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))) 
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my')

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change_password.html'
    success_message = "Password changed successfully!"
    success_url = reverse_lazy('profiles:my')
