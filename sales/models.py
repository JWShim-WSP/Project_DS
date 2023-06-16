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
    unit_price = models.FloatField(blank=True)
    quantity = models.PositiveIntegerField(blank=True)
    net_price = models.FloatField(blank=True)

    inventory_status = models.CharField(max_length=30, null=True) # 'Yes' or 'No' will be set in 'save' of Position
    net_profit = models.FloatField(blank=True, null=True)
    margin_percentage = models.FloatField(blank=True, null=True)
    position_sold = models.BooleanField(default=False, null=True)

    # need to open for date selection for importing a new data from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.net_price = self.unit_price * self.quantity
        if self.product.inventory >= self.quantity: # short of inventory
            self.net_profit = (self.unit_price - self.product.average_unit_price_KRW) * self.quantity
            self.margin_percentage = ((self.unit_price - self.product.average_unit_price_KRW) / self.product.average_unit_price_KRW) * 100
            self.inventory_status = "Yes"
        else:
            self.inventory_status = "No"
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

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    positions = models.ManyToManyField(Position)
    #if multi positions are allowed, it is not easy to trace down Sale and Position
    #position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # This will be automatically calculated through the signal of changes of positions in signals.py
    total_net_price = models.FloatField(blank=True, null=True)
    total_net_profit = models.FloatField(blank=True, null=True)
    
    tax_cost = models.FloatField(default=0, blank=True, null=True)
    vat_cost = models.FloatField(default=0, blank=True, null=True)
    delivery_cost = models.FloatField(default=0, blank=True, null=True)
    extra_cost = models.FloatField(default=0, blank=True, null=True)

    final_profit = models.FloatField(blank=True, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # need to open the selectin of date for importing a new date from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        #if self.total_price is None: /* Signal from m2m 'post_add' or 'post_remove' will make the total_price
        #    self.total_price = self.position.price
        return super().save(*args, **kwargs)

    # Have all positions, and calculate the sum of all prices of the postions to get total_price in signal.py
    def get_positions(self):
        return self.positions.all()

    def get_absolute_url(self):
        return reverse('sales:salesdetails', kwargs={'pk':self.pk})

    def positions_ids(self):
        return ', '.join([str(a.id)+': ' + a.product.name for a in self.positions.all()])
    
    positions_ids.short_description = "Positions ID"

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"Sales for the amount of ${self.total_net_price}"


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)


