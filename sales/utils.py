import uuid, base64
from customers.models import Customer
from products.models import Product
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
 
 # 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

def get_salesman_from_id(val):
    salesman = Profile.objects.get(id=val)
    return salesman.user.username

def get_customer_from_id(val):
    customer = Customer.objects.get(id=val)
    return customer.name

def get_product_from_id(val):
    product = Product.objects.get(id=val)
    return product.name

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# function to add value labels
def addlabels(x, y, chart_type, sum_by):
    total_sum = 0
    for i in range(len(x)):
        total_sum += y[i]
        if (chart_type == 'Horizontal Bar Chart'):
            if (sum_by == 'quantity'):
                plt.text(y[i], i, int(y[i]), va='center')
            else:
                plt.text(y[i], i, '{:,.2f}'.format(y[i]), va='center')
        else:
            if (sum_by == 'quantity'):
                plt.text(i, y[i], int(y[i]), ha='center')
            else:
                plt.text(i, y[i], '{:,.2f}'.format(y[i]), ha='center')

    if (sum_by == 'quantity'):
        return int(total_sum)
    else:
        return '{:,.2f}'.format(total_sum)

def get_chart(chart_type, data, key_by, sum_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))

    #d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    #plt.title(f"Sales Total: {addlabels(d[key], d['total_price'], chart_type)}")
    # if data frame is merged_df, 'price' should be the base of sum instead of 'total_price'
    d = data.groupby(key_by, as_index=False)[sum_by].agg('sum')
    plt.title(f"Total: {addlabels(d[key_by], d[sum_by], chart_type, sum_by)}")

    if chart_type == 'Bar Chart':
        #plt.bar(d[key], d['total_price'])
        plt.xlabel(key_by, color='purple')
        plt.ylabel(sum_by, color='blue')
        sns.barplot(x=key_by, y=sum_by, data=d)
    elif chart_type == 'Horizontal Bar Chart':
        #plt.barh(d[key], d['total_price'])
        plt.xlabel(sum_by, color='purple')
        plt.ylabel(key_by, color='blue')
        sns.barplot(orient='h', x=sum_by, y=key_by, data=d)
    elif chart_type == 'Pie Chart':
        plt.pie(data=d, x=sum_by, labels=d[key_by].values, autopct='%1.1f%%')
    elif chart_type == 'Line Chart':
        plt.plot(d[key_by], d[sum_by], color='green', marker='o', linestyle='dashed')
    else:
        print('No...!!!')
    plt.tight_layout()
    chart = get_graph()
    return chart
