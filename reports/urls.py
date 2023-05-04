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
    create_report_view,
    ReportListView,
    ReportDetailView,
    render_pdf_view,
    UploadTemplateView,
    csv_upload_view,
)

app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name='main'),
    path('<int:pk>/', ReportDetailView.as_view(), name='detail'),
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path('save/', create_report_view, name='create-report'),
    path('upload/', csv_upload_view, name='upload'),
    path('<int:pk>/pdf/', render_pdf_view, name='pdf'),
]