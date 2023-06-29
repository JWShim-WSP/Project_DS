from import_export import fields, resources
from products.models import ProductGroup, Product, Purchase
from customers.models import Supplier
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class ProductResource(resources.ModelResource):
    supplier = fields.Field(
        column_name='supplier',
        attribute='supplier',
        widget=ForeignKeyWidget(Supplier, field='name'))

    supplier = fields.Field(
        column_name='product_type',
        attribute='product_type',
        widget=ForeignKeyWidget(ProductGroup, field='name'))

    # customers can be expessed through 'ManyToManyWidget' for exporting, but not working for import
    #customers = fields.Field(
    #    column_name='customers',
    #    attribute='customers',
    #    widget= ManyToManyWidget(Customer, field='name', separator='|')
    #)

    class Meta:
        model = Product
        # enumerate the fields to export
        fields = ('id', 'name', 'currency', 'price', 'moq', 'price_quantity_base', 'supplier', 'customers', 'created', 'updated', 'product_type', 'remark')
        export_order = fields

class PurchaseResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, field='name'))

    class Meta:
        model = Purchase
        # enumerate the fields to export
        fields = ('id', "product", "unit_price", "quantity", "net_price", "added_cost", "added_price", "ex_rate_to_KRW", "net_price_KRW", "custom_tax_KRW", 'transport_cost_KRW', "bank_cost_KRW", "delivery_cost_KRW", "added_price_KRW", "status")
        export_order = fields

