from django.db import models
from django.urls import reverse

# Create your models here.

PRODUCT_TYPE_CHOICES = (
    ('Sensor', 'Sensor'),
    ('Plasma Torch', 'Plasma Torch'),
    ('Pump', 'Pump'),
    ('Pressure', 'Pressure'),
    ('Etc', 'Etc'),
)

PRODUCT_CHOICES_FOR_SEARCH = (
    ('All', 'All'),
    ('Sensor', 'Sensor'),
    ('Plasma Torch', 'Plasma Torch'),
    ('Pump', 'Pump'),
    ('Pressure', 'Pressure'),
    ('Etc', 'Etc'),
)

class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in US dollars $')
    # you need to make 'created' as selectable to import a new data from a file
    created = models.DateTimeField()
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remark = models.TextField(max_length=1024, blank=True)
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)

    def get_absolute_url(self):
        return reverse('products:productdetails', kwargs={'pk':self.pk})

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"id: {self.id}, {self.name}-{self.product_type}"
