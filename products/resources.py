from import_export import resources
from products.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        # enumerate the fields to export
        fields = ('id', 'name', 'price', 'created', 'updated', 'product_type', 'remark')
        export_order = fields

