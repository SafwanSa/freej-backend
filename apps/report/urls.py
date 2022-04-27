from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.ReportView.as_view())
]
