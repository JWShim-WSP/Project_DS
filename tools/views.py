from django.shortcuts import render

# Create your views here.
def tools_main_view(request):
    return render(request, 'tools/main.html')
