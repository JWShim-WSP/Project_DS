from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

# Create your models here.
LANGUAGE_CHOICE = (
    ('English', 'English'),
    ('Korean', 'Korean'),
)

MENU_CHOICE = (
    ('Top', 'Top'),
    ('Side', 'Side'),
    ('Bottom', 'Bottom'),
)

def default_datetime_for_my_class():
    return datetime(2050,1,1)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    language = models.CharField(max_length=12, choices=LANGUAGE_CHOICE, default="English")
    menubar = models.CharField(max_length=12, choices=MENU_CHOICE, default="Top")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    licensed_by = models.DateField(default=default_datetime_for_my_class)

    def __str__(self):
        return self.user.username
    
    # write your get_absolute_url instance method here for DetailView
    def get_absolute_url(self):
        return reverse('myadmin:memberdetails', kwargs={'pk':self.id})
