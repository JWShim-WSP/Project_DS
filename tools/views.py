from django.shortcuts import render

# Create your views here.
def ToolsMain(request):
    return render(request, 'tools/main.html')
