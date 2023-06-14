from django.shortcuts import render, redirect
from .models import Bulletin, Comment
from django.urls import reverse, reverse_lazy
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from profiles.models import Profile
from hitcount.views import HitCountDetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

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
        likers_connected = get_object_or_404(Bulletin, slug=self.kwargs['slug'])
        liked = False
        if likers_connected.likers.filter(user=self.request.user).exists():
            liked = True
        context['number_of_likers'] = likers_connected.number_of_likers()
        context['post_is_liked'] = liked

        comments_connected = Comment.objects.filter(CommentPost=self.get_object())
        number_of_comments = comments_connected.count()
        context['comments'] = comments_connected
        context['no_of_comments'] = number_of_comments
        context['comment_form'] = CommentForm()
        return context

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None

                new_comment = Comment(content=content , author = self.request.user.profile , CommentPost=self.get_object() , parent=parent)
                new_comment.save()
        return redirect(self.request.path_info)


class BulletinCreatePost(CreateView):
    form_class = PostForm
    template_name = 'bulletin/post_form.html'

    def form_valid(self, form):
        newPost=form.save(commit=False)
        newPost.poster = self.request.user.profile
        form = newPost
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("bulletin:bstBulletin")

class BulletinUpdate(UpdateView):
    model = Bulletin
    form_class = PostForm
    template_name = 'bulletin/post_form.html'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.poster == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "You cannot update other poster's post!")
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse("bulletin:bstBulletin")

class BulletinDelete(DeleteView):
    model = Bulletin
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("bulletin:bstBulletin")

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = Bulletin.objects.get(slug=slug)
        if not obj.poster.user == self.request.user:
            messages.warning(self.request, "You cannot delete other poster's post!")
        return obj

def BulletinLike(request, slug):
    post = get_object_or_404(Bulletin, id=request.POST.get('post_id'))
    liker_user = Profile.objects.get(user=request.user)

    if post.likers.filter(user=request.user).exists():
        post.likers.remove(liker_user)
    else:
        post.likers.add(liker_user)

    return HttpResponseRedirect(reverse('bulletin:bstBulletinContent', kwargs={'slug':slug}))
