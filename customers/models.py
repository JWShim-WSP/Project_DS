from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=120, unique=True)
    logo = models.ImageField(upload_to='customers', default='no_picture.png')
    email = models.EmailField(max_length=256, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=265, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('customers:customerdetails', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}"
 
    class Meta:
        ordering = ['-created']

class Supplier(models.Model):
    name = models.CharField(max_length=120, unique=True)
    logo = models.ImageField(upload_to='suppliers', default='no_picture.png')
    email = models.EmailField(max_length=256, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=265, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remark = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('customers:supplierdetails', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}"
 
    class Meta:
        ordering = ['-created']
