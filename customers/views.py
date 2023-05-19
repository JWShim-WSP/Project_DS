from django.shortcuts import render
from django.urls import reverse
from .models import Customer
from .forms import CustomerForm
from .resources import CustomerResource
from profiles.forms import FormatForm

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def customer_list_view(request):
    if (request.method == 'POST'):
        dataset = CustomerResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstcustomer.{format}"
        return response
    else:
        p = Paginator(Customer.objects.all(), 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)
        
        form_class = FormatForm()
            
        context = {
            'object_list': object_list,
            'form': form_class,
        }
        return render(request, 'customers/customers_list.html', context)


@staff_member_required
def customer_detail_view(request, pk):
    customer = Customer.objects.get(pk=pk)
    form = CustomerForm(request.POST or None, request.FILES or None, instance=customer)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': customer,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'customers/customer_detail.html', context)

@staff_member_required
def customer_add_view(request):
    form = CustomerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('customers:customerlist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'customers/customer_detail.html', context)

@staff_member_required
def customer_delete_view(request, pk):
    customer = Customer.objects.get(pk=pk)

    if request.method == 'POST':
        customer.delete()
        return HttpResponseRedirect(reverse('customers:customerlist'))
    else:
        context = {
            'profile': customer,
        }
        return render(request, 'customers/customer_confirm_delete.html', context)
