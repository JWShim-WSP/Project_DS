from django.db import models
from django.urls import reverse

# Create your models here.

PRODUCT_CHOICES = (
    ('#1', 'sensor'),
    ('#2', 'torch'),
    ('#3', 'pump'),
    ('#4', 'etc'),
)

class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in US dollars $')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remark = models.TextField(max_length=1024, blank=True)
    product_type = models.CharField(max_length=2, choices=PRODUCT_CHOICES)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}-{self.created.strftime('%d/%m/%Y')}"