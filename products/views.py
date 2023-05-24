from django.shortcuts import render
from django.urls import reverse
from .models import Product, PRODUCT_TYPE_CHOICES
from .forms import ProductForm, ProductSearchForm
from sales.forms import CHART_CHOICES
from .resources import ProductResource
from profiles.forms import FormatForm
import pandas as pd
from sales.utils import get_chart
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductSearchForm


# Create your views here.
@staff_member_required
def product_list_view(request):
    products_df = None
    chart = None
    no_data = None

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
        chart_type = request.GET.get('chart_type')
        results_by = request.GET.get('results_by')

        if (results_by == None or results_by == 'All'):
            products_qs = Product.objects.all()
        else:
            products_qs = Product.objects.filter(product_type=results_by)

        p = Paginator(products_qs, 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)
        
        if len(products_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            key_by = 'name' # the names of the products will be used for 'key'

            sum_by = 'price' # no use in product df for 'sum' operation
        
            products_df = pd.DataFrame(products_qs.values())
            products_df['created'] = products_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            products_df['updated'] = products_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression

            chart = get_chart(chart_type, products_df, key_by, sum_by)

            products_df = products_df.to_html(classes='table text-center table-striped', justify='center')

        else:
            no_data = 'No data is available in this date range'

        form_class = FormatForm()
        search_form = ProductSearchForm()

        context = {
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'products_df': products_df,
            'chart': chart,
            'no_data': no_data
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
