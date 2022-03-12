from django.urls import include, path
from . import views

urlpatterns = [
    path('access/', views.CustomTokenObtainPairView.as_view()),
    path('refresh/', views.CustomTokenRefreshView.as_view()),
]
