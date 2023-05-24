from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale, Position
from products.models import PRODUCT_CHOICES_FOR_SEARCH
from profiles.forms import FormatForm
from .forms import SalesSearchForm, SaleForm, PositionForm, PositionSearchForm, CHART_CHOICES, RESULT_CHOICES, SUM_CHOICES 
from .resources import SaleResource, PositionResource
from reports.forms import ReportForm
import pandas as pd
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .utils import get_customer_from_id, get_salesman_from_id, get_product_from_id, get_chart


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# MVT (Model, View, and Template) for Django applications

@login_required
def sales_home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    YoYchart = None
    MoMchart = None
    Monthchart = None
    chart = None
    no_data = None

    if (request.method == 'POST'):
        dataset = SaleResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstsales.{format}"
        return response
    else:
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        chart_type = request.GET.get('chart_type')
        key_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if date_from and date_to:
            sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        else:
            sales_qs = Sale.objects.all()

        if len(sales_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            if key_by == None:
                key_by = RESULT_CHOICES[0][0]
                
            if sum_by == None:
                sum_by = SUM_CHOICES[0][0]

            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            #sales_df['sales_id'] = sales_df['id'] # or, you can add a new 'sales_id' column

            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                    'position_id': pos.id,
                    'product': pos.product.name,
                    'quantity': pos.quantity,
                    'unit_price': pos.unit_price,
                    'added_cost': pos.added_cost,
                    'net_price': pos.net_price,
                    'added_price': pos.added_price,
                    'ex_rate_to_KRW': pos.ex_rate_to_KRW,
                    'added_cost_KRW': pos.added_cost_KRW,
                    'net_price_KRW': pos.net_price_KRW,
                    'added_price_KRW': pos.added_price_KRW,
                    'sales_id': pos.get_sales_id(), # reverse relationship to 'Sale' from 'Position'
                    }
                    positions_data.append(obj)

            search_form = SalesSearchForm(request.POST or None)
            form_class = FormatForm()

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            chart = get_chart(chart_type, merged_df, key_by, sum_by)
            merged_df = merged_df.to_html(classes='table text-center table-striped', justify='center')
        else:
            no_data = 'No data is available in this date range'

    context = {
        'search_form': search_form,
        'form': form_class,
        'merged_df': merged_df,
        'chart': chart,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sales_list.html'
    # context_object_name = 'sales' ; if you want a unique object name

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sales_detail.html'


# You can implement the Views above in FBV (Function Based View)
# in the urls:
# path('sales/', sale_list_view, name='listview')
# path('sales/<pk>/', sale_detail_view, name='detailview')
@staff_member_required
def sales_list_view(request):
    merged_df = None
    chart = None
    no_data = None

    if (request.method == 'POST'):
        dataset = SaleResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstsales.{format}"
        return response
    else:
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        chart_type = request.GET.get('chart_type')
        key_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if date_from and date_to:
            sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        else:
            sales_qs = Sale.objects.all()

        p = Paginator(sales_qs, 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)

        if len(sales_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            if key_by == None:
                key_by = RESULT_CHOICES[0][0]
                
            if sum_by == None:
                sum_by = SUM_CHOICES[0][0]

            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            #sales_df['sales_id'] = sales_df['id'] # or, you can add a new 'sales_id' column

            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                    'position_id': pos.id,
                    'product': pos.product.name,
                    'quantity': pos.quantity,
                    'unit_price': pos.unit_price,
                    'added_cost': pos.added_cost,
                    'net_price': pos.net_price,
                    'added_price': pos.added_price,
                    'ex_rate_to_KRW': pos.ex_rate_to_KRW,
                    'added_cost_KRW': pos.added_cost_KRW,
                    'net_price_KRW': pos.net_price_KRW,
                    'added_price_KRW': pos.added_price_KRW,
                    'sales_id': pos.get_sales_id(), # reverse relationship to 'Sale' from 'Position'
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            chart = get_chart(chart_type, merged_df, key_by, sum_by)
            merged_df = merged_df.to_html(classes='table text-center table-striped', justify='center')
        else:
            no_data = 'No data is available in this date range'     

        search_form = SalesSearchForm()
        form_class = FormatForm()

        context = {
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'merged_df': merged_df,
            'chart': chart,
            'no_data': no_data,
        }
        return render(request, 'sales/sales_list.html', context)


@staff_member_required
def sales_detail_view(request, pk):
    sales = Sale.objects.get(pk=pk)
    form = SaleForm(request.POST or None, instance=sales)
    confirm = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': sales,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'sales/sales_detail.html', context)

@staff_member_required
def sales_add_view(request):
    form = SaleForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('sales:saleslist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'sales/sales_detail.html', context)

@staff_member_required
def sales_delete_view(request, pk):
    sales = Sale.objects.get(pk=pk)

    if request.method == 'POST':
        sales.delete()
        return HttpResponseRedirect(reverse('sales:saleslist'))
    else:
        context = {
            'profile': sales,
        }
        return render(request, 'sales/sales_confirm_delete.html', context)


@staff_member_required
def positions_list_view(request):
    positions_df = None
    chart = None
    no_data = None
    
    if (request.method == 'POST'):
        dataset = PositionResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstposition.{format}"
        return response
    else:
        chart_type = request.GET.get('chart_type')
        results_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if chart_type == None:
            chart_type = CHART_CHOICES[0][0]
        
        if (results_by == None or results_by == 'All'):
            positions_qs = Position.objects.all()
        else:
            positions_qs = Position.objects.filter(product__product_type=results_by)

        p = Paginator(positions_qs, 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)

        if len(positions_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            key_by = 'product' # use the name of products for 'key'

            if sum_by == None:
                sum_by = SUM_CHOICES[0][0]
            
            positions_df = pd.DataFrame(positions_qs.values())
            positions_df['product_id'] = positions_df['product_id'].apply(get_product_from_id)
            positions_df['created'] = positions_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            positions_df.rename({'product_id': 'product'}, axis=1, inplace=True)
            chart = get_chart(chart_type, positions_df, key_by, sum_by)
            positions_df = positions_df.to_html(classes='table text-center table-striped', justify='center')
        else:
            no_data = 'No data is available in this date range'     

        search_form = PositionSearchForm()
        form_class = FormatForm()
            
        context = {
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'positions_df': positions_df,
            'chart': chart,
            'no_data': no_data,
        }
        return render(request, 'sales/positions_list.html', context)


@staff_member_required
def position_detail_view(request, pk):
    position = Position.objects.get(pk=pk)
    form = PositionForm(request.POST or None, instance=position)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': position,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'sales/position_detail.html', context)

@staff_member_required
def position_add_view(request):
    form = PositionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('sales:positionlist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'sales/position_detail.html', context)

@staff_member_required
def position_delete_view(request, pk):
    position = Position.objects.get(pk=pk)

    if request.method == 'POST':
        position.delete()
        return HttpResponseRedirect(reverse('sales:positionlist'))
    else:
        context = {
            'profile': position,
        }
        return render(request, 'sales/position_confirm_delete.html', context)
