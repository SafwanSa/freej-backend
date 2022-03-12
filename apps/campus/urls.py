from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.CampusesView.as_view()),
    path('<int:campus_id>/buildings/', views.BuildingsView.as_view()),
]
