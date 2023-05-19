from django.shortcuts import render
from django.urls import reverse
from .models import Product
from .forms import ProductForm
from .resources import ProductResource
from profiles.forms import FormatForm

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def product_list_view(request):
    if (request.method == 'POST'):
        dataset = ProductResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstproduct.{format}"
        return response
    else:
        p = Paginator(Product.objects.all(), 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)
        
        form_class = FormatForm()
            
        context = {
            'object_list': object_list,
            'form': form_class,
        }
        return render(request, 'products/products_list.html', context)


@staff_member_required
def product_detail_view(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': product,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'products/product_detail.html', context)

@staff_member_required
def product_add_view(request):
    form = ProductForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('products:productlist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'products/product_detail.html', context)

@staff_member_required
def product_delete_view(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('products:productlist'))
    else:
        context = {
            'profile': product,
        }
        return render(request, 'products/product_confirm_delete.html', context)
