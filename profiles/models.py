from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify
from .utils import get_random_code
from django.db.models import Q

# Create your models here.
LANGUAGE_CHOICE = (
    ('English', 'English'),
    ('Korean', 'Korean'),
)

MENU_CHOICE = (
    ('Top', 'Top'),
    ('Button', 'Button'),
)

def default_datetime_for_my_class():
    return datetime(2050,1,1)

class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(receiver=profile) | Q(sender=profile))

        exclude_list = set([])
        for rel in qs:
            exclude_list.add(rel.sender)
            exclude_list.add(rel.receiver)

        available = [profile for profile in profiles if profile not in exclude_list]
        
        #accepted = set([]) # no duplicate 
        #for rel in qs:
        #    if rel.status == 'accepted': # we are going to exclude all in the Relationship list
        #        accepted.add(rel.receiver)
        #        accepted.add(rel.sender)
        # all people as friend candidates, except for me and whom already in the list
        #available = [profile for profile in profiles if profile not in accepted]
        return available

    def get_all_profiles_send_waiting(self, sender):
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile))

        receiver_waiting_profiles = [rel.receiver for rel in qs if rel.status == 'send']
        return receiver_waiting_profiles

    def get_all_profiles_receive_waiting(self, receiver):
        profile = Profile.objects.get(user=receiver)
        qs = Relationship.objects.filter(Q(receiver=profile))

        sender_waiting_profiles = [rel.sender for rel in qs if rel.status == 'send']
        return sender_waiting_profiles

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    language = models.CharField(max_length=12, choices=LANGUAGE_CHOICE, default="English")
    menubar = models.CharField(max_length=12, choices=MENU_CHOICE, default="Top")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    licensed_by = models.DateField(default=default_datetime_for_my_class)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()
    
    def get_all_posters_posts(self):
        return self.posts.all()
    
    def get_posts_no(self):
        return self.posts.all().count()
        # As you specified with 'related_name', you can use 'posts' instead of 'bulletin_set'

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for post in posts:
            total_liked += post.likers.all().count()
        return total_liked

    def get_likes_given_no(self):
        return self.post_likers.all().count()
    
    # write your get_absolute_url instance method here for DetailView
    def get_absolute_url(self):
        return reverse('profiles:profile-detail-view', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        if not self.first_name and self.user.first_name:
            self.first_name = self.user.first_name
        if not self.last_name and self.user.last_name:
            self.last_name = self.user.last_name
        if not self.email and self.user.email:
            self.email = self.user.email

        if not self.slug: # just created and signaled by User from Admin
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name), allow_unicode=True)
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()), allow_unicode=True)
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user.username)
            self.slug = to_slug
        return super(Profile, self).save(*args, **kwargs)


STATUS_CHOICES = [
    ('send', 'send'),
    ('accepted', 'accepted'),
]

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

