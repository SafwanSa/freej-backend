from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.CampusAndBuildingAnnouncementsView.as_view()),
    path('commercial/', views.CommercialAnnouncementsView.as_view()),
    path('send/', views.SendAnnouncementView.as_view()),
    path('<int:pk>/', views.DeleteAnnouncementView.as_view())
]
