"""
Function-Based View (FBV)
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-Based View (CBV)
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
Pass Converter
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: Univerally unique identifier
    # path('<int:year>/<str:month>', views.CBV or FBV, name = 'names')
    # path('<path:path>', views.FBV or CBV, name='names')
    # in view.py file, def name(request, year, month):
    #                  and with context dictionary for passing parameters to html file.
"""

from django.urls import path
from .views import home_view, SaleListView, SaleDetailView, sale_list_view, sale_detail_view, position_detail_view

app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home'),
    # permission required cannot be implemented for now for CBV
    #path('sales/', SaleListView.as_view(), name='list'),
    #path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
    # go for FBV this time!
    path('sales/position/<int:pk>/', position_detail_view, name='position_detail'),
    path('sales/', sale_list_view, name='slaes_list'),
    path('sales/<int:pk>/', sale_detail_view, name='sales_detail'),
]