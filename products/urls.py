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
from .views import (
    inventory_reset_view,
    group_list_view, 
    group_detail_view, 
    group_add_view, 
    group_delete_view,

    product_list_view, 
    product_detail_view, 
    product_add_view, 
    product_delete_view,

    purchase_positions_list_view,
    purchase_position_detail_view,
    purchase_position_add_view,
    purchase_position_delete_view,
    )

app_name = 'products'

urlpatterns = [
    # permission required cannot be implemented for now for CBV
    #path('sales/', SaleListView.as_view(), name='list'),
    #path('sales/<pk>/', SaleDetailView.as_view(), name='detail'),
    # go for FBV this time!
    path('', product_list_view, name='productlist'),
    path('inventoryreset', inventory_reset_view, name='inventoryreset'),
    path('page/<int:page>/', product_list_view, name='productlist'),
    path('<int:pk>/', product_detail_view, name='productdetails'),
    path('add/', product_add_view, name='product-add'),
    path('<int:pk>/delete/', product_delete_view, name='product-delete'),
    path('group/', group_list_view, name='grouplist'),
    path('group/<int:pk>/', group_detail_view, name='groupdetails'),
    path('group/add/', group_add_view, name="group-add"),
    path('group/<int:pk>/delete/', group_delete_view, name='group-delete'),
    path('positions/', purchase_positions_list_view, name='positionlist'),
    path('position/<int:pk>/', purchase_position_detail_view, name='positiondetails'),
    path('position/add/', purchase_position_add_view, name='position-add'),
    path('position/<int:pk>/delete/', purchase_position_delete_view, name='position-delete'),
]