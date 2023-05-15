from django.shortcuts import render
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def customer_list_view(request):
    qs = Customer.objects.all()
    return render(request, 'customers/customers_list.html', {'object_list':qs})

@staff_member_required
def customer_detail_view(request, pk):
    obj = Customer.objects.get(pk=pk)
    # or
    # obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'customers/customer_detail.html', {'object':obj})
