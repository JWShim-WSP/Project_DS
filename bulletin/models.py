from django.db import models
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import Profile
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
# Let's go for Class Based View for Click Count

class Bulletin(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=256, unique=True)
    content = models.TextField(max_length=4096)
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    post_Date = models.DateField(default=timezone.now)
    update_Date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    likers = models.ManyToManyField(Profile, blank=True, related_name='post_likers')

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
            self.slug = slugify(self.title, allow_unicode=True)
        return super(Bulletin, self).save(*args, **kwargs)
    
    def get_likers(self):
        return self.likers.all()

    def number_of_likers(self):
        return self.likers.all().count()
    
    def number_of_comments(self):
        return self.comment_set.all().count()
    
    def current_hit_count(self):
        return self.hit_count.hits
    
    class Meta:
        ordering = ['-post_Date']

class Comment(models.Model):
    CommentPost = models.ForeignKey(Bulletin , on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    post_Date = models.DateTimeField(default=timezone.now)
    update_Date = models.DateField(auto_now=True)
    parent = models.ForeignKey('self' , blank=True , on_delete=models.CASCADE , related_name='replies')

    class Meta:
        ordering=['-post_Date']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    