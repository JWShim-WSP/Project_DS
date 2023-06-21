from django.shortcuts import render
from django.urls import reverse
from .models import Customer, Supplier
from .forms import CustomerForm, SupplierForm
from .resources import CustomerResource, SupplierResource
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
        p = Paginator(Customer.objects.all().order_by('name'), 10)
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

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('customers:customerlist'))

    context = {
        'profile': customer,
        'form': form,
        'confirm': False,
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

@staff_member_required
def supplier_list_view(request):
    if (request.method == 'POST'):
        dataset = SupplierResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstsupplier.{format}"
        return response
    else:
        p = Paginator(Supplier.objects.all().order_by('name'), 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)
        
        form_class = FormatForm()
            
        context = {
            'object_list': object_list,
            'form': form_class,
        }
        return render(request, 'customers/suppliers_list.html', context)


@staff_member_required
def supplier_detail_view(request, pk):
    supplier = Supplier.objects.get(pk=pk)
    form = SupplierForm(request.POST or None, request.FILES or None, instance=supplier)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('customers:supplierlist'))

    context = {
        'profile': supplier,
        'form': form,
        'confirm': False,
    }
    return render(request, 'customers/supplier_detail.html', context)

@staff_member_required
def supplier_add_view(request):
    form = SupplierForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('customers:supplierlist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'customers/supplier_detail.html', context)

@staff_member_required
def supplier_delete_view(request, pk):
    supplier = Supplier.objects.get(pk=pk)

    if request.method == 'POST':
        supplier.delete()
        return HttpResponseRedirect(reverse('customers:supplierlist'))
    else:
        context = {
            'profile': supplier,
        }
        return render(request, 'customers/supplier_confirm_delete.html', context)
