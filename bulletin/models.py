from django.db import models
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profile
from django.utils.text import slugify




# Create your models here.
# Let's go for Class Based View for Click Count

class Bulletin(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True)
    post_Date = models.DateField(auto_now_add=True)
    update_Date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    content = models.TextField(max_length=4096)

    # Let's count the clicks (Hits) of visitors
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def __str__(self):
        return f"{self.title} {self.poster} {self.post_Date}"

    # write your get_absolute_url instance method here for DetailView
    def get_absolute_url(self):
        return reverse('bulletin:bstBulletinContent', kwargs={'slug':self.slug})
        #return reverse('bulletin:bstBulletinContent', kwargs={'pk':self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Bulletin, self).save(*args, **kwargs)

    def current_hit_count(self):
        return self.hit_count.hits
