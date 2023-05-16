from import_export import resources
from sales.models import Position, Sale
from import_export.fields import Field

class PositionResource(resources.ModelResource):
    product = Field()
    class Meta:
        model = Position
        # enumerate the fields to export
        fields = ('id', 'product', 'quantity', 'price', 'created')
        export_order = fields

    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    def dehydrate_product(self, obj):
        return obj.product.name


class SaleResource(resources.ModelResource):
    positions = Field()
    customer = Field()
    salesman = Field()
    class Meta:
        model = Sale
        # enumerate the fields to export
        fields = ('id', 'transaction_id', 'positions', 'total_price', 'customer', 'salesman', 'created', 'updated')
        export_order = fields

    # position_id is a better information than product.name of the position
    #def dehydrate_positions(self, obj):
    #    position_names = []
    #    for position in obj.get_positions():
    #        position_names.append(position.product.name + ', ')
    #    return position_names
    
    # To change (dehydrate) the display from number('1 or 0') to text ('Ture or False')
    def dehydrate_customer(self, obj):
        return obj.customer.name
        
    def dehydrate_salesman(self, obj):
        return obj.salesman.user.username
    
