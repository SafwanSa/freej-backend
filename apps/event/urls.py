from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.EventViewset, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('applications/<int:event_id>/', views.EventApplicationView.as_view())
]
