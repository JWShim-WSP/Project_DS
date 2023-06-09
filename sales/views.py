from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale, Position
from products.models import PRODUCT_CHOICES_FOR_SEARCH, Purchase, Product
from profiles.forms import FormatForm
from .forms import SalesSearchForm, ExecutedSaleForm, SaleForm, PositionForm, PositionSearchForm, current_year, CHART_CHOICES, RESULT_CHOICES, POSITION_SUM_CHOICES, SALES_SUM_CHOICES
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

import calendar
# Create your views here.
# MVT (Model, View, and Template) for Django applications

@login_required
def sales_dashboard_view(request):

    chart1 = chart2 = chart3 = chart4 = None
    no_data1 = None
    no_data2 = None
    no_data3 = None
    no_data4 = None

    sales_positions_qs = Position.objects.order_by('inventory_status', 'position_sold')
    purchase_positions_qs = Purchase.objects.order_by('status')
    products_qs = Product.objects.order_by('-updated')
    sales_status_qs = Sale.objects.order_by('delivery_completed')

    # Make YoY chart for final_profit
    sales_qs = Sale.objects.all()
    if len(sales_qs) > 0:
        chart_type = 'Bar Chart'
        key_by = 'year'
        sum_by = 'final_profit'
        sales_df = pd.DataFrame(sales_qs.values())
        sales_df['year'] = sales_df['created'].apply(lambda x: x.strftime('%Y')) # lambda argument: expression
        chart1 = get_chart(chart_type, sales_df, key_by, sum_by)
    else:
        if request.user.profile.language == "Korean":
            no_data1 = '관련 자료 정보가 없습니다.'
        else:
            no_data1 = 'No data is available.'

    year_from = year_to = current_year()
    date_from = str(year_from) + '-' + str(1) + '-' + str(1)
    date_to = str(year_to) + '-' + str(12) + '-' + str(31)
    sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
    if len(sales_qs) > 0:
        chart_type = 'Bar Chart'
        key_by = 'year_month'
        sum_by = 'final_profit'
        sales_df = pd.DataFrame(sales_qs.values())
        sales_df['year_month'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m')) # lambda argument: expression
        chart2 = get_chart(chart_type, sales_df, key_by, sum_by)
    else:
        if request.user.profile.language == "Korean":
            no_data2 = '관련 자료 정보가 없습니다.'
        else:
            no_data2 = 'No data is available.'

    sales_qs = Sale.objects.all()
    # Make YoY chart for total sales revenue
    if len(sales_qs) > 0:
        chart_type = 'Bar Chart'
        key_by = 'year'
        sum_by = 'total_net_price'
        sales_df = pd.DataFrame(sales_qs.values())
        sales_df['year'] = sales_df['created'].apply(lambda x: x.strftime('%Y')) # lambda argument: expression
        chart3 = get_chart(chart_type, sales_df, key_by, sum_by)
    else:
        if request.user.profile.language == "Korean":
            no_data3 = '관련 자료 정보가 없습니다.'
        else:
            no_data3 = 'No data is available.'

    # Make Monthly chart for this year sales revenue
    year_from = year_to = current_year()
    date_from = str(year_from) + '-' + str(1) + '-' + str(1)
    date_to = str(year_to) + '-' + str(12) + '-' + str(31)
    sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
    if len(sales_qs) > 0:
        chart_type = 'Bar Chart'
        key_by = 'year_month'
        sum_by = 'total_net_price'
        sales_df = pd.DataFrame(sales_qs.values())
        sales_df['year_month'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m')) # lambda argument: expression
        chart4 = get_chart(chart_type, sales_df, key_by, sum_by)
    else:
        if request.user.profile.language == "Korean":
            no_data4 = '관련 자료 정보가 없습니다.'
        else:
            no_data4 = 'is available in this date range'

    context = {
        'object_list_products': products_qs,
        'object_list_positions': sales_positions_qs,
        'object_list_purchase': purchase_positions_qs,
        'object_list_sales': sales_status_qs,
        'current_year': current_year,
        'chart1': chart1,
        'chart2': chart2,
        'chart3': chart3,
        'chart4': chart4,
        'no_data1': no_data1,
        'no_data2': no_data2,
        'no_data3': no_data3,
        'no_data4': no_data4,
    }
    return render(request, 'sales/dashboard.html', context)

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
        merged_df = None
        chart = None
        no_data = None
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        year_from = request.GET.get('year_from')
        year_to = request.GET.get('year_to')
        month_from = request.GET.get('month_from')
        month_to = request.GET.get('month_to')
        chart_type = request.GET.get('chart_type')
        key_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')
        sales_complete_by = request.GET.get('sales_complete_by')

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

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if date_from and date_to:
            sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')
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
                sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')

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
                sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from).order_by('-updated')

            else:# you choose no period (All years and All months)
                sales_qs = Sale.objects.all().order_by('-updated')

        if sales_complete_by != None and sales_complete_by != 'All':
            if sales_complete_by == "Yes":
                sales_qs = sales_qs.filter(delivery_completed=True)
            else: # not completed
                sales_qs = sales_qs.filter(delivery_completed=False)

        # no pagination needed for sales list
        #p = Paginator(sales_qs, 10)
        #try:
        #    object_list = p.get_page(request.GET.get("page"))
        #except:
        #    object_list = p.get_page(1)
        object_list = sales_qs

        if len(sales_qs) > 0:
            if chart_type == None:
                chart_type = CHART_CHOICES[0][0]

            if key_by == None:
                key_by = RESULT_CHOICES[0][0]
                
            if sum_by == None:
                sum_by = SALES_SUM_CHOICES[0][0]

            sales_df = pd.DataFrame(sales_qs.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['year'] = sales_df['created'].apply(lambda x: x.strftime('%Y')) # lambda argument: expression
            sales_df['year_month'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m')) # lambda argument: expression
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d')) # lambda argument: expression
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            #sales_df['sales_id'] = sales_df['id'] # or, you can add a new 'sales_id' column
            
            # Warning! You cannot have multiple sales on the same positions. Sales should be one on one with Position
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj = {
                    'position_id': pos.id,
                    'product': pos.product.name,
                    'unit_price': pos.unit_price,
                    'quantity': pos.quantity,
                    'net_price': pos.net_price,
                    'inventory_status': pos.inventory_status,
                    'net_profit': pos.net_profit,
                    'margin_percentage': pos.margin_percentage,
                    'sales_id': pos.get_sales_id(), # reverse relationship to 'Sale' from 'Position'
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            chart = get_chart(chart_type, merged_df, key_by, sum_by)
            merged_df = merged_df.to_html(classes='table text-center table-striped', justify='center')
        else:
            if request.user.profile.language == "Korean":
                no_data = '관련 자료 정보가 없습니다.'
            else:
                no_data = 'No data is available.'     

        search_form = SalesSearchForm()
        form_class = FormatForm()
        report_form = ReportForm()
        products_qs = Product.objects.all().order_by('-updated')

        context = {
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'report_form': report_form,
            'merged_df': merged_df,
            'chart': chart,
            'no_data': no_data,
            'object_list_products': products_qs,
    }
        return render(request, 'sales/sales_list.html', context)


@staff_member_required
def sales_detail_view(request, pk):
    sales = Sale.objects.get(pk=pk)
    form = ExecutedSaleForm(request.POST or None, instance=sales)
    qs = sales.positions.all()
    confirm = False
    delivery_completed = True

    if request.method == "POST":
        for position in qs:
            if position.inventory_status == False: # check if the inventory is supplied at this moment
                if position.product.inventory >= position.quantity: # now it is to complete the delivery
                    position.position_sold = False                    
                    position.save() # this will make the product.inventory updated by Signaling!!!
                    position.position_sold = True
                    position.save(update_fields=['position_sold'])
                else:
                    delivery_completed = False

        if sales.delivery_completed == False: # if it was blocked before
            if delivery_completed == True:
                sales.delivery_completed = True
                sales.save()
        else:
            sales.error # should not happen!!!

        confirm = True

    context = {
        'profile': sales,
        'form': form,
        'confirm': confirm,
        'position_avail': True
    }
    return render(request, 'sales/sales_detail.html', context)

@staff_member_required
def sales_add_view(request):
    form = SaleForm(request.POST or None)
    sales = Sale()
    confirm = False

    qs = Position.objects.filter(position_sold=False)
    if qs:
        position_avail = True
        if request.method == "POST":
            if form.is_valid():
                form.save()
                sales.transaction_id = form.cleaned_data['transaction_id']
                confirm = True
    else:
        position_avail = False

    context = {
        'profile': sales,
        'form': form,
        'confirm': confirm,
        'position_avail': position_avail
    }
    return render(request, 'sales/sales_detail.html', context)

@staff_member_required
def sales_delete_view(request, pk):
    sales = Sale.objects.get(pk=pk)
    positions = sales.positions.all()

    if request.method == 'POST':
        for position in positions:
            # compensate the inventory before save position as it will signal to Product's inventory
            if position.inventory_status == True:
                position.product.inventory += position.quantity
                position.product.save(update_fields=['inventory'])
            position.position_sold = False
            position.save(update_fields=['position_sold'])
        sales.delete()
        return HttpResponseRedirect(reverse('sales:saleslist'))
    else:
        context = {
            'profile': sales,
        }
        return render(request, 'sales/sales_confirm_delete.html', context)


@staff_member_required
def positions_list_view(request):
    
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
        sales_complete_by = request.GET.get('sales_complete_by')
        results_by = request.GET.get('results_by')
        sum_by = request.GET.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        if date_from and date_to:
            positions_qs = Position.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
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
                positions_qs = Position.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

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
                positions_qs = Position.objects.filter(created__date__lte=date_to, created__date__gte=date_from)

            else:# you choose no period (All years and All months)
                positions_qs = Position.objects.all()


        if chart_type == None:
            chart_type = CHART_CHOICES[0][0]
        
        if (results_by != None and results_by != 'All'):
            positions_qs = positions_qs.filter(product__product_type=results_by)
        
        if sales_complete_by != None and sales_complete_by != 'All':
            if sales_complete_by == "Yes":
                positions_qs = positions_qs.filter(position_sold=True)
            else: # not completed
                positions_qs = positions_qs.filter(position_sold=False)
            
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
                sum_by = POSITION_SUM_CHOICES[0][0]
            
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

        search_form = PositionSearchForm()
        form_class = FormatForm()
        products_qs = Product.objects.all().order_by('-updated')
            
        context = {
            'object_list': object_list,
            'form': form_class,
            'search_form': search_form,
            'positions_df': positions_df,
            'chart': chart,
            'no_data': no_data,
            'object_list_products': products_qs,
        }
        return render(request, 'sales/positions_list.html', context)


@staff_member_required
def position_detail_view(request, pk):
    position = Position.objects.get(pk=pk)
    form = PositionForm(request.POST or None, instance=position)
    confirm = False
    
    # let's remember the quantity for any changes!!!
    if position.inventory_status == True:
        position_quantity = position.quantity
        position_product = position.product
    else:
        position_quantity = 0

    products_qs = Product.objects.all().order_by('-updated')

    if request.method == "POST":
        if form.is_valid():
            # before it saves the new data, let's compensate the product inventory for update
            if position_quantity:
                if position_product == position.product: # not changed
                    position.product.inventory += position_quantity
                    position.product.save(update_fields=['inventory'])
                else: # changed
                    position_product.inventory += position_quantity
                    position_product.save(update_fields=['inventory'])
            form.save()
            confirm = True

    context = {
        'profile': position,
        'form': form,
        'confirm': confirm,
        'object_list_products': products_qs,
}
    return render(request, 'sales/position_detail.html', context)

@staff_member_required
def position_add_view(request):
    form = PositionForm(request.POST or None)
    position = Position()
    products_qs = Product.objects.all().order_by('-updated')
    confirm = False

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
