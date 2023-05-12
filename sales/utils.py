import uuid, base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_salesman_from_id(val):
    salesman = Profile.objects.get(id=val)
    return salesman.user.username

def get_customer_from_id(val):
    customer = Customer.objects.get(id=val)
    return customer.name

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_key(res_by):
    if res_by == '#1':
        key = 'transaction_id'
    elif res_by == '#2':
        key = 'position_id'
    elif res_by == '#3':
        key = 'created'
    elif res_by == '#4':
        key = 'customer'
    elif res_by == '#5':
        key = 'salesman'

    return key

# function to add value labels
def addlabels(x, y, chart_type):
    sales_total = 0
    for i in range(len(x)):
        sales_total += y[i]
        if (chart_type == '#2'):
            plt.text(y[i], i, '{:,.2f}'.format(y[i]), va='top')
        else:
            plt.text(i, y[i], '{:,.2f}'.format(y[i]), ha='center')
    return '{:,.2f}'.format(sales_total)

def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    plt.title(f"Sales Total: {addlabels(d[key], d['total_price'], chart_type)}")

    if chart_type == '#1':
        plt.bar(d[key], d['total_price'])
        plt.xlabel(key, color='purple')
        plt.ylabel("Total Price", color='blue')
        #sns.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#2':
        plt.barh(d[key], d['total_price'])
        plt.xlabel("Total Price", color='purple')
        plt.ylabel(key, color='blue')
        #sns.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#3':
        plt.pie(data=d, x='total_price', labels=d[key].values, autopct='%1.1f%%')
    elif chart_type == '#4':
        plt.plot(d[key], d['total_price'], color='green', marker='o', linestyle='dashed')
    else:
        print('No...!!!')
    plt.tight_layout()
    chart = get_graph()
    return chart
