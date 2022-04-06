from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('offers', views.OfferViewSet, basename='offers')
router.register('requests', views.RequestViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),
]
