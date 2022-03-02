from django.urls import include, path
from . import views

urlpatterns = [
    path('access/', views.CustomTokenObtainPairView.as_view()),
    path('refresh/', views.CustomTokenRefreshView.as_view()),
    path('error/', views.ExampleErrorView.as_view()),
    path('', views.UserView.as_view())
]
