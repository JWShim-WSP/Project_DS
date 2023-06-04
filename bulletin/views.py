from django.shortcuts import render
from .models import Bulletin
from django.urls import reverse, reverse_lazy
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from hitcount.views import HitCountDetailView


# Create your views here.

# Let's go to CBV than FBV above
class bstBulletin(LoginRequiredMixin, ListView):
    model = Bulletin
    context_object_name = 'posts' # you can omit this to use default name, 'object'
    template_name = 'bulletin/bstbulletin.html' # you can omit this to use default template name, 'Post_list.html'

    def get_queryset(self, *args, **kwargs):
        p = Paginator(Bulletin.objects.order_by('-update_Date'), 10)
        try:
            return p.get_page(self.request.GET.get("page"))
        except:
            return p.get_page(1)


class BulletinDetailView(LoginRequiredMixin, HitCountDetailView):
    model = Bulletin
    context_object_name = 'post'
    template_name = 'bulletin/bulletincontent.html'
    slug_field = 'slug'
    # set to True to count the hit (everybody can see this post!)
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BulletinDetailView, self).get_context_data(**kwargs)
        context.update({'popular_posts':Bulletin.objects.order_by('-hit_count_generic__hits')[:3],})
        return context

class BulletinCreatePost(CreateView):
    form_class = PostForm
    template_name = 'bulletin/post_form.html'

    def get_context_data(self, **kwargs):
        context = super(BulletinCreatePost, self).get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        return context

    def form_valid(self, form):
        newPost=form.save(commit=False)
        newPost.poster = self.request.user.profile
        form = newPost
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("bulletin:bstBulletin")


class BulletinUpdate(UpdateView):
    model = Bulletin
    context_object_name = 'post'
    form_class = PostForm
    template_name = 'bulletin/post_form.html'

    def get_context_data(self, **kwargs):
        context = super(BulletinUpdate, self).get_context_data(**kwargs)
        post = context['post'] 
        thePost = Bulletin.objects.get(pk=post.id)
        post_form = PostForm(instance=thePost)
        context['form'] = post_form 
        context.update({'profile': Profile.objects.get(user=self.request.user)})
        return context

    def get_success_url(self):
        return reverse("bulletin:bstBulletin")


class BulletinDelete(DeleteView):
    model = Bulletin
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("bulletin:bstBulletin")
