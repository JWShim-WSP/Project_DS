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

def getProductGroupChoices():
    qs = ProductGroup.objects.all()
    return qs.insert(0, 'All')


class ProductGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    remark = models.TextField(max_length=1024, blank=True)

    def get_absolute_url(self):
        return reverse('products:groupdetails', kwargs={'pk':self.pk})

    def __str__(self):
        return f"{self.name}"
 

class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    currency = models.CharField(choices=CURRENCIES, max_length=30)
    #price = models.FloatField(help_text='in US dollars $')
    price = models.FloatField(blank=False)
    moq = models.IntegerField(blank=True, default=1)
    price_quantity_base = models.PositiveIntegerField(default=10)
    remark = models.TextField(max_length=1024, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='product_supplier')
    customers = models.ManyToManyField(Customer, blank=True, related_name='product_customers')
    product_type = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    inventory = models.IntegerField(default=0)
    average_unit_price = models.FloatField(default=0)
    average_unit_price_KRW = models.FloatField(default=0)
    average_ex_rate_to_KRW = models.FloatField(default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_net_price_KRW = models.FloatField(default=0)
    total_added_price_KRW = models.FloatField(default=0)
    # you need to make 'created' as selectable to import a new data from a file
    created = models.DateTimeField(default=timezone.now)
    #created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('products:productdetails', kwargs={'pk':self.pk})

    def get_customers(self):
        return self.customers.all()

    def customers_ids(self):
        #return ', '.join([str(a.id)+': ' + a.name for a in self.customers.all()])
        return ', '.join([a.name for a in self.customers.all()])
    
    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f"ID: {self.id}, {self.name}-{self.product_type}"

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_purchase")
    unit_price = models.FloatField(blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    net_price = models.FloatField(blank=True)
    added_cost = models.FloatField(default=0)
    added_price = models.FloatField(blank=True)

    ex_rate_to_KRW = models.FloatField(blank=False)
    net_price_KRW = models.FloatField(blank=True)
    custom_tax_KRW = models.FloatField(default=0)
    transport_cost_KRW = models.FloatField(default=0)
    bank_cost_KRW = models.FloatField(default=0)
    delivery_cost_KRW = models.FloatField(default=0)
    added_price_KRW = models.FloatField(blank=True)
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
