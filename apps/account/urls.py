from django.urls import include, path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('register-confirmation/', views.ConfirmRegisterView.as_view()),

    path('access/', views.ResidentTokenObtainPairView.as_view()),
    path('refresh/', views.ResidentTokenRefreshView.as_view()),
]
