from django.db import models
from django.urls import reverse

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default='no_picture.png')
    email = models.EmailField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=265, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('customers:customerdetails', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}"
 
