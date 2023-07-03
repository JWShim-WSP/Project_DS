from django.shortcuts import render
from django.urls import reverse
from .models import ProductGroup, Product, Purchase
from .forms import ProductGroupForm, ProductForm, ProductSearchForm, PurchaseForm, PurchaseSearchForm, PURCHASE_SUM_CHOICES, PRODUCT_SUM_CHOICES
from sales.forms import CHART_CHOICES, current_year
from sales.models import Sale, Position
from .resources import ProductGroupResource, ProductResource, PurchaseResource
from profiles.forms import FormatForm
import pandas as pd
from sales.utils import get_chart, get_product_from_id
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import calendar

# Create your views here.

@staff_member_required
def inventory_reset_view(request):
    confirm = False

    if request.method == 'POST':
        sales_qs = Sale.objects.all()
        for sales in sales_qs:
            sales.delete()

        positons_qs = Position.objects.all()
        for position in positons_qs:
            position.delete()

        purchase_qs = Purchase.objects.all()
        for purchase in purchase_qs:
            purchase.delete()

        products_qs = Product.objects.all()
        for product in products_qs:
            new_purchase = Purchase()
            new_purchase.product = product
            new_purchase.quantity = product.inventory
            new_purchase.unit_price = product.average_unit_price
            new_purchase.ex_rate_to_KRW = product.average_ex_rate_to_KRW
            new_purchase.status = "Stocked"
            new_purchase.save() # this will signal to create new product information, too.

        confirm = True
    
    context = {
        'confirm': confirm,
    }
    return render(request, 'products/inventory_reset_confirm.html', context)


@staff_member_required
def group_list_view(request):
    if request.method == 'POST':
        dataset = ProductGroupResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstproductgroup.{format}"
        return response
    else:
        product_group = ProductGroup.objects.all().order_by('name')
        form_class = FormatForm()

        context = {
            'object_list': product_group,
            'form': form_class,
        }
        return render(request, 'products/group_list.html', context)


@staff_member_required
def group_delete_view(request, pk):
    product_group = ProductGroup.objects.get(pk=pk)

    if request.method == 'POST':
        product_group.delete()
        return HttpResponseRedirect(reverse('products:grouplist'))
    else:
        context = {
            'profile': product_group,
        }
        return render(request, 'products/group_confirm_delete.html', context)

@staff_member_required
def group_detail_view(request, pk):
    product_group = ProductGroup.objects.get(pk=pk)
    form = ProductGroupForm(request.POST or None, instance=product_group)
    confirm = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True


    context = {
        'profile': product_group,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'products/group_detail.html', context)

@staff_member_required
def group_add_view(request):
    form = ProductGroupForm(request.POST or None)
    confirm = False
    product_group = ProductGroup()

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True
            product_group.name = form.cleaned_data['name']

    context = {
        'profile': product_group,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'products/group_detail.html', context)

@staff_member_required
def product_list_view(request):

    if request.method == 'POST':
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
        products_df = None
        chart = None
        no_data = None

        chart_type = request.GET.get('chart_type')
        type_by = request.GET.get('type_by')
        sum_by = request.GET.get('sum_by')
        supplier_by = request.GET.get('supplier_by')

        if type_by == None or type_by == 'All':
            products_qs = Product.objects.all().order_by('-updated')
        else:
            products_qs = Product.objects.filter(product_type=type_by).order_by('-updated')
        
        if supplier_by is not None:
            products_qs = products_qs.filter(supplier=supplier_by).order_by('-updated')

        # No pagination for product list
        #p = Paginator(products_qs, 10)
        #try:
        #    object_list = p.get_page(request.GET.get("page"))
        #except:
        #    object_list = p.get_page(1)
        object_list = products_qs
        
        if len(products_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            key_by = 'name' # the names of the products will be used for 'key'

            if sum_by == None:
                sum_by = PRODUCT_SUM_CHOICES[0][0]
        
            products_df = pd.DataFrame(products_qs.values())
            products_df['created'] = products_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            products_df['updated'] = products_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression

            chart = get_chart(chart_type, products_df, key_by, sum_by)

            products_df = products_df.to_html(classes='table text-center table-striped', justify='center')

        else:
            if request.user.profile.language == "Korean":
                no_data = '관련 자료 정보가 없습니다.'
            else:
                no_data = 'No data is available.'

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

    if request.method == "POST":
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
    form = ProductForm(request.POST or None, request.FILES or None)
    confirm = False
    product = Product()

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True
            product.name = form.cleaned_data['name']

    context = {
        'profile': product,
        'form': form,
        'confirm': confirm,
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

@staff_member_required
def purchase_positions_list_view(request):
    
    if (request.method == 'POST'):
        dataset = PurchaseResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstpurchase.{format}"
        return response
    else:
        positions_df = None
        chart = None
        no_data = None

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        year_from = request.GET.get('year_from')
        year_to = request.GET.get('year_to')
        month_from = request.GET.get('month_from')
        month_to = request.GET.get('month_to')

        if year_from != None: # if it is not None, it should be a 'str'
            year_from = int(year_from)
        else:
            year_from = 0
        if year_to != None: # if it is not None, it should be a 'str'
            year_to = int(year_to)
        else:
            year_to = 0
        if month_from != None:
            month_from = int(month_from)
        else:
            month_from = 0
        if month_to != None:
            month_to = int(month_to)
        else:
            month_to = 0
        chart_type = request.GET.get('chart_type')
        results_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if date_from and date_to:
            positions_qs = Purchase.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')
        else:
            if year_from:
                if not year_to: # if no year end specified, make it to 'year_from'
                    year_to = year_from
                if year_from > year_to: # if order is reversed
                    temp = year_from
                    year_from = year_to
                    year_to = temp

                if month_from: #specified month period too
                    if not month_to: # if no month end specified, make it to 'month_from'
                        month_to = month_from
                    if month_from > month_to:
                        temp = month_from
                        month_from = month_to
                        month_to = temp
                    date_from = str(year_from) + '-' + str(month_from) + '-' + str(1)
                    date_to = str(year_to) + '-' + str(month_to) + '-' + str(calendar.monthrange(year_to, month_to)[1])
                else: # no month specified to make 12 months
                    date_from = str(year_from) + '-' + str(1) + '-' + str(1)
                    date_to = str(year_to) + '-' + str(12) + '-' + str(calendar.monthrange(year_to, 12)[1])
                positions_qs = Purchase.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')

            elif month_from: #you want to see MoM of the year
                if not month_to: # if no month end specified, make it to 'month_from'
                    month_to = month_from
                if month_from > month_to:
                    temp = month_from
                    month_from = month_to
                    month_to = temp
                year_from = year_to = current_year()
                date_from = str(year_from) + '-' + str(month_from) + '-' + str(1)
                date_to = str(year_to) + '-' + str(month_to) + '-' + str(calendar.monthrange(year_to, month_to)[1])
                positions_qs = Purchase.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')

            else:# you choose no period (All years and All months)
                positions_qs = Purchase.objects.all().order_by('-updated')

        if chart_type == None:
            chart_type = CHART_CHOICES[0][0]
        
        if (results_by != None and results_by != 'All'):
            positions_qs = positions_qs.filter(product__product_type=results_by)

        # no pagination for positions needed
        #p = Paginator(positions_qs, 10)
        #try:
        #    object_list = p.get_page(request.GET.get("page"))
        #except:
        #    object_list = p.get_page(1)
        object_list = positions_qs

        if len(positions_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            key_by = 'product' # use the name of products for 'key'

            if sum_by == None:
                sum_by = PURCHASE_SUM_CHOICES[0][0]
            
            positions_df = pd.DataFrame(positions_qs.values())
            positions_df['product_id'] = positions_df['product_id'].apply(get_product_from_id)
            positions_df['created'] = positions_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            positions_df.rename({'product_id': 'product'}, axis=1, inplace=True)
            chart = get_chart(chart_type, positions_df, key_by, sum_by)
            positions_df = positions_df.to_html(classes='table text-center table-striped', justify='center')
        else:
            if request.user.profile.language == "Korean":
                no_data = '관련 자료 정보가 없습니다.'
            else:
                no_data = 'No data is available.'     

        search_form = PurchaseSearchForm()
        form_class = FormatForm()
        products_qs = Product.objects.order_by('-updated')
            
        context = {
            'object_list_products': products_qs,
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'positions_df': positions_df,
            'chart': chart,
            'no_data': no_data,
        }
        return render(request, 'products/positions_list.html', context)


@staff_member_required
def purchase_position_detail_view(request, pk):
    position = Purchase.objects.get(pk=pk)
    form = PurchaseForm(request.POST or None, instance=position)
    confirm = False
    products_qs = Product.objects.all().order_by('-updated')

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': position,
        'form': form,
        'confirm': confirm,
        'object_list_products': products_qs,
    }
    return render(request, 'products/position_detail.html', context)

@staff_member_required
def purchase_position_add_view(request):
    form = PurchaseForm(request.POST or None)
    position = Purchase()
    confirm = False
    products_qs = Product.objects.all().order_by('-updated')

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True
            position.product = form.cleaned_data['product']

    context = {
        'profile': position,
        'form': form,
        'confirm': confirm,
        'object_list_products': products_qs,
    }
    return render(request, 'products/position_detail.html', context)

@staff_member_required
def purchase_position_delete_view(request, pk):
    position = Purchase.objects.get(pk=pk)

    if request.method == 'POST':
        position.delete()
        return HttpResponseRedirect(reverse('products:positionlist'))
    else:
        context = {
            'profile': position,
        }
        return render(request, 'products/position_confirm_delete.html', context)
