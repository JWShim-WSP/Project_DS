from django.db import models

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
    product_type = models.CharField(max_length=2, choices=PRODUCT_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.created.strftime('%d/%m/%Y')}"