from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(upload_to='avatars', default='no_picture.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    # write your get_absolute_url instance method here for DetailView
    def get_absolute_url(self):
        return reverse('myadmin:memberdetails', kwargs={'pk':self.id})
