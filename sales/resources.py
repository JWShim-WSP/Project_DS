from import_export import fields, resources
from sales.models import Position, Sale
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class PositionResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, field='name'))

    #product = Field() # this is for dehydrate
    class Meta:
        model = Position
        # enumerate the fields to export
        fields = ("id", "product", "quantity", "unit_price", "added_cost", "net_price", "added_price", "ex_rate_to_KRW", "added_cost_KRW", "net_price_KRW", "added_price_KRW", 'created')
        export_order = fields

    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False') ==> Let's use ForeignKeyWidget for importing not just for exporting
    #def dehydrate_product(self, obj):
    #    return obj.product.name

class SaleResource(resources.ModelResource):
    
    #positions = Field() # this is for dehydrate which will be replaced with ManytoMany and ForeignKey widgets for importing too not just for exporting
    #customer = Field()
    #salesman = Field()

    # if you give 'product' for 'position' in exporting, then you cannot import again with 'id'
    #positions = fields.Field(
    #    column_name='positions',
    #    attribute='positions',
    #    widget= ManyToManyWidget(Position, field='product', separator='|')
    #)

    customer = fields.Field(
        column_name='customer',
        attribute='customer',
        widget=ForeignKeyWidget(Customer, field='name'))

    salesman = fields.Field(
        column_name='salesman',
        attribute='salesman',
        widget=ForeignKeyWidget(Profile, field='user__username'))
    
    class Meta:
        model = Sale
        # enumerate the fields to export
        fields = ('id', 'transaction_id', 'positions', "total_net_price", "total_added_price", "total_net_price_KRW", "total_added_price_KRW", 'customer', 'salesman', 'created', 'updated')
        export_order = fields

    #position_id is a better information than product.name of the position
    #def dehydrate_positions(self, obj):
    #    position_ids = []
    #    for position in obj.get_positions():
    #        position_ids.append(str(position.id) + '('+ position.product.name +'), ')
    #    return position_ids
    
    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    #def dehydrate_customer(self, obj):
    #    return obj.customer.name
        
    #def dehydrate_salesman(self, obj):
    #    return obj.salesman.user.username
    
