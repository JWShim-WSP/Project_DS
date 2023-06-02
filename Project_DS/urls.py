"""
URL configuration for Project_DS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view

urlpatterns = [
    path('', include('sales.urls', namespace='sales')),
    path('bulletin/', include('bulletin.urls', namespace='bulletin')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('products/', include('products.urls', namespace='products')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('my_profile/', include('profiles.urls', namespace='profiles')),
    path('myadmin/', include('myadmin.urls', namespace='myadmin')),
    path('tools/', include('tools.urls', namespace='tools')),
    path('calculator/', include('calculator.urls', namespace='calculator')),
    path('calendarwithevent/', include('calendarwithevent.urls', namespace='calendarwithevent')),
    path('excurrency/', include('excurrency.urls', namespace='excurrency')),
    path('worldtime/', include('worldtime.urls', namespace='worldtime')),
    path('todolist/', include('todolist.urls', namespace='todolist')),
    path('emailsend/', include('emailsend.urls', namespace='emailsend')),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)