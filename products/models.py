from django.db import models
from django.urls import reverse
from django.utils import timezone
from customers.models import Customer, Supplier
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

CURRENCIES = (
    ("USD", "US Dollar"),
    ("EUR", "Euro"),
    ("KRW", "South Korean Won"),
    ("BTC", "Bitcoin"),
    ("JPY", "Japanese Yen"),
    ("CNY", "Chinese Yuan"),
    ("GBP", "British Pound Sterling"),
)

PURCHASE_STATUS = (
    ('prep', 'Preparation'),
    ('PO', 'PO issued'),
    ('Invoice', 'Invoice paid'),
    ('Arrived', 'Arrived'),
    ('Stocked', 'Stocked'),
)

class Product(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    currency = models.CharField(choices=CURRENCIES, max_length=30, null=True)
    #price = models.FloatField(help_text='in US dollars $')
    price = models.FloatField()
    moq = models.IntegerField(blank=True, default=1, null=True)
    price_quantity_base = models.PositiveIntegerField(default=10)
    remark = models.TextField(max_length=1024, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, related_name='product_supplier')
    customers = models.ManyToManyField(Customer, blank=True, related_name='product_customers')
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES)
    inventory = models.IntegerField(default=0)
    average_unit_price = models.FloatField(default=0, null=True)
    average_unit_price_KRW = models.FloatField(default=0, null=True)
    average_ex_rate_to_KRW = models.FloatField(default=0, null=True)
    total_quantity = models.PositiveIntegerField(default=0, null=True)
    total_net_price_KRW = models.FloatField(default=0, null=True)
    total_added_price_KRW = models.FloatField(default=0, null=True)
    # you need to make 'created' as selectable to import a new data from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('products:productdetails', kwargs={'pk':self.pk})

    def get_customers(self):
        return self.customers.all()

    def customers_ids(self):
        return ', '.join([str(a.id)+': ' + a.name for a in self.customers.all()])
    
    customers_ids.short_description = "Positions ID"

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"ID: {self.id}, {self.name}-{self.product_type}"

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_purchase")
    unit_price = models.FloatField()
    quantity = models.PositiveIntegerField()
    net_price = models.FloatField()
    added_cost = models.FloatField(default=0)
    added_price = models.FloatField()

    ex_rate_to_KRW = models.FloatField()
    net_price_KRW = models.FloatField()
    custom_tax_KRW = models.FloatField(default=0)
    transport_cost_KRW = models.FloatField(default=0)
    bank_cost_KRW = models.FloatField(default=0)
    delivery_cost_KRW = models.FloatField(default=0)
    added_price_KRW = models.FloatField()
    status=models.CharField(choices=PURCHASE_STATUS, max_length=30)

    # need to open for date selection for importing a new data from a file
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    #created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.net_price = self.unit_price * self.quantity
        self.added_price = self.net_price + self.added_cost

        self.net_price_KRW = self.net_price * self.ex_rate_to_KRW
        self.added_price_KRW = (self.added_price * self.ex_rate_to_KRW) + self.custom_tax_KRW + self.transport_cost_KRW + self.bank_cost_KRW + self.delivery_cost_KRW
        # Finally, let's signal to 'Product' so that inventory can be added with self.quantity.
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:positiondetails', kwargs={'pk':self.pk})

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"ID: {self.id}, Product: {self.product.name}, Quantity: {self.quantity}"
