from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale, Position
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_chart, get_sum_by, get_key_by


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# MVT (Model, View, and Template) for Django applications

@login_required
def home_view(request):

    bst_positions = Position.objects.all()
    bst_sales = Sale.objects.all()

    sales_df = None
    positions_df = None
    merged_df = None
    df_transaction = None
    df_position = None
    df_created = None
    df_customer = None
    df_salesman = None
    chart = None
    no_data = None

    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
        sum_by = request.POST.get('sum_by')

        #qs = Sale.objects.all()
        # filter the data with lte (less than equal) and gte (greater than equal)
        sales_qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if len(sales_qs) > 0:
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
                    'price': pos.price,
                    'sales_id': pos.get_sales_id(), # reverse relationship to 'Sale' from 'Position'
                    #'position_id': sale.position.id,
                    #'product': sale.position.product.name,
                    #'quantity': sale.position.quantity,
                    #'price': sale.position.price,
                    #'sales_id': sale.id,
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            sum_by = get_sum_by(sum_by)
            key_by = get_key_by(results_by)

            # sum by the choice of 'price' or 'quantity' to show in graph
            df_transaction = merged_df.groupby('transaction_id', as_index=False)[sum_by].agg('sum') # aggregate
            df_position = merged_df.groupby('position_id', as_index=False)[sum_by].agg('sum') # aggregate
            df_created = merged_df.groupby('created', as_index=False)[sum_by].agg('sum') # aggregate
            df_customer = merged_df.groupby('customer', as_index=False)[sum_by].agg('sum') # aggregate
            df_salesman = merged_df.groupby('salesman', as_index=False)[sum_by].agg('sum') # aggregate

            #chart = get_chart(chart_type, sales_df, results_by)
            chart = get_chart(chart_type, merged_df, key_by, sum_by)

            sales_df = sales_df.to_html(classes='table table-striped text-center', justify='center')
            positions_df = positions_df.to_html(classes='table table-striped text-center', justify='center')
            merged_df = merged_df.to_html(classes='table table-striped text-center', justify='center')

            df_transaction = df_transaction.to_html(classes='table table-striped text-center', justify='center')
            df_position = df_position.to_html(classes='table table-striped text-center', justify='center')
            df_created = df_created.to_html(classes='table table-striped text-center', justify='center')
            df_customer = df_customer.to_html(classes='table table-striped text-center', justify='center')
            df_salesman = df_salesman.to_html(classes='table table-striped text-center', justify='center')
        else:
            no_data = 'No data is availablein in this date range'

    context = {
        'bst_positions': bst_positions,
        'bst_sales': bst_sales,
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df_transaction': df_transaction,
        'df_position': df_position,
        'df_created': df_created,
        'df_customer': df_customer,
        'df_salesman': df_salesman,
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
def sale_list_view(request):
    qs = Sale.objects.all()
    return render(request, 'sales/sales_list.html', {'object_list':qs})

@staff_member_required
def sale_detail_view(request, pk):
    obj = Sale.objects.get(pk=pk)
    # or
    # obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sales_detail.html', {'object':obj})

@staff_member_required
def position_detail_view(request, pk):
    obj = Position.objects.get(pk=pk)
    # or
    # obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/position_detail.html', {'object':obj})
