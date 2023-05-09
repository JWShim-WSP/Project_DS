from django.urls import path
from . import views

"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
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

app_name = 'calendarwithevent'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendarwithevent'),
    # Events View
    path('calendarevents', views.CalendarEvents.as_view(), name='calendarevents'),
    # CRUD patterns for EventList
    path("calendarevents/add/", views.EventCreate.as_view(), name="event-add"),
    path("calendarevents/item/<int:pk>/", views.EventUpdate.as_view(), name="event-update"),
    path("calendarevents/<int:pk>/delete/", views.EventDelete.as_view(), name="event-delete"),
]
    
