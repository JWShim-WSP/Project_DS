from import_export import resources
from customers.models import Customer, Supplier

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        # enumerate the fields to export
        fields = ('id', 'name', 'email', "cc", 'phone_number', 'remark')
        export_order = fields

class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        # enumerate the fields to export
        fields = ('id', 'name', 'email', "cc", 'phone_number', 'remark')
        export_order = fields

