from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='customers', default='no_picture.png')
    email = models.EmailField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=265, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)
 
