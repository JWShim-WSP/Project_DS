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
    unit_price = models.FloatField(blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    net_price = models.FloatField(blank=True)

    inventory_status = models.BooleanField(default=False) # 'True' or 'False' will be set in 'save' of Position
    net_profit = models.FloatField(blank=True)
    margin_percentage = models.FloatField(blank=True)
    position_sold = models.BooleanField(default=False)

    # need to open for date selection for importing a new data from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try: # it could come from Purchase signal or Sales signal
            if (kwargs['update_fields'] != ['inventory_status']) and (kwargs['update_fields'] != ['position_sold']): # Hey, you came here from Signal of Purchase or Sales
                self.net_price = self.unit_price * self.quantity
                self.net_profit = (self.unit_price - self.product.average_unit_price_KRW) * self.quantity
                if self.product.average_unit_price_KRW:
                    self.margin_percentage = ((self.unit_price - self.product.average_unit_price_KRW) / self.product.average_unit_price_KRW) * 100
                else:
                    self.margin_percentage = 0
                if self.product.inventory >= self.quantity: # short of inventory
                    self.inventory_status = True
                else:
                    self.inventory_status = False
        except: # comes from normal Postion save
            self.net_price = self.unit_price * self.quantity
            self.net_profit = (self.unit_price - self.product.average_unit_price_KRW) * self.quantity
            if self.product.average_unit_price_KRW:
                self.margin_percentage = ((self.unit_price - self.product.average_unit_price_KRW) / self.product.average_unit_price_KRW) * 100
            else:
                self.margin_percentage = 0
            if self.product.inventory >= self.quantity: # short of inventory
                self.inventory_status = True
            else:
                self.inventory_status = False
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

    @property
    def get_inventory_with_quantity(self):
        if (self.inventory_status):
            return self.product.inventory + self.quantity
        else:
            return self.product.inventory

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"ID: {self.id}, Product: {self.product.name}, Quantity: {self.quantity}"

class Sale(models.Model):
    transaction_id = models.CharField(max_length=1024)
    positions = models.ManyToManyField(Position)
    #if multi positions are allowed, it is not easy to trace down Sale and Position
    #position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # This will be automatically calculated through the signal of changes of positions in signals.py
    total_net_price = models.FloatField(blank=True)
    total_net_profit = models.FloatField(blank=True)
    
    # tax/vat will be included in the price to customers, or it should not be counted here as will be returned to the government
    #tax_cost = models.FloatField(default=0, null=True)
    #vat_cost = models.FloatField(default=0, null=True)
    delivery_cost = models.FloatField(default=0)
    extra_cost = models.FloatField(default=0)

    final_profit = models.FloatField(blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # need to open the selectin of date for importing a new date from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    delivery_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # No transaction_id from generate_code. This will be typed at form.
        #if self.transaction_id == "":
        #    self.transaction_id = generate_code()
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
    
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"Sales for the amount of {self.total_net_price}(KRW)"


class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file_name)


