from django.urls import include, path
from . import views

urlpatterns = [
    path('access/', views.ResidentTokenObtainPairView.as_view()),
    path('refresh/', views.ResidentTokenRefreshView.as_view()),
]
