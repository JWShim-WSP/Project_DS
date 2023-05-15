from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def product_list_view(request):
    qs = Product.objects.all()
    return render(request, 'products/products_list.html', {'object_list':qs})

@staff_member_required
def product_detail_view(request, pk):
    obj = Product.objects.get(pk=pk)
    # or
    # obj = get_object_or_404(Sale, pk=pk)
    return render(request, 'products/product_detail.html', {'object':obj})
