from import_export import resources
from customers.models import Customer

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        # enumerate the fields to export
        fields = ('id', 'name')
        export_order = fields
