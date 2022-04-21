from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router2 = DefaultRouter()
router.register('offers', views.OfferViewSet, basename='offers')
router.register('requests', views.RequestViewSet, basename='requests')
router2.register('', views.RequestApplicationsViewSet, basename='requests-applications')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:post_id>/applications/', include(router2.urls)),
    path('<int:post_id>/reviews/', views.ReviewView.as_view()),
]
