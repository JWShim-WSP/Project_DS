from django.db import models
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone
from .utils import generate_code
from django.urls import reverse

# Create your models here.

class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    net_unit_price = models.FloatField()

    added_cost = models.FloatField()

    total_net_price = models.FloatField(blank=True)
    total_added_price = models.FloatField(blank=True)

    ex_rate_to_KRW = models.FloatField()
    added_cost_KRW = models.FloatField()
    total_net_price_KRW = models.FloatField(blank=True)
    total_added_price_KRW = models.FloatField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_net_price = self.net_unit_price * self.quantity
        self.total_added_price = self.total_net_price + self.added_cost

        self.total_net_price_KRW = self.total_net_price * self.ex_rate_to_KRW
        self.total_added_price_KRW = (self.total_added_price * self.ex_rate_to_KRW) + self.added_cost_KRW
        return super().save(*args, **kwargs)

    def get_sales_id(self):
        # reverse relationship to sale (sale_set: set of 'Sale' model with the first item)
        sale_obj = self.sale_set.first()
        return sale_obj.id
    
    def get_absolute_url(self):
        return reverse('sales:positiondetails', kwargs={'pk':self.pk})
    
    def get_sales_customer(self):
        # reverse relationship to sale (sale_set: set of 'Sale' model with the first item)
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name

    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    #if multi positions are allowed, it is not easy to trace down Sale and Position
    #position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # This will be automatically calculated through the signal of changes of positions in signals.py
    total_net_price = models.FloatField(blank=True, null=True)
    total_added_price = models.FloatField(blank=True, null=True)
    total_net_price_KRW = models.FloatField(blank=True, null=True)
    total_added_price_KRW = models.FloatField(blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        #if self.total_price is None: /* Signal from m2m 'post_add' or 'post_remove' will make the total_price
        #    self.total_price = self.position.price
        return super().save(*args, **kwargs)

    # Have all positions, and calculate the sum of all prices of the postions to get total_price in signal.py
    def get_positions(self):
        return self.positions.all()

    def get_absolute_url(self):
        return reverse('sales:salesdetails', kwargs={'pk':self.pk})
    
    def __str__(self):
        return f"Sales for the amount of ${self.total_price}"


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)


