from api.views import ClientViewSet, DriverViewSet, RideViewSet, LocationViewSet, UserViewSet, VehicleViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('client', ClientViewSet, basename='client')
router.register('driver', DriverViewSet, basename='driver')
router.register('ride', RideViewSet, basename='ride')
router.register('location', LocationViewSet, basename='location')
router.register('user', UserViewSet, basename='user')
router.register('vehicle', VehicleViewSet, basename='vehicle')


urlpatterns = [
    path("login/", views.login),
    path("register/", views.register),
    path("", include(router.urls)),
]
    # [
    # path('client/', include(router.urls)),
    # path('driver/', include(router.urls)),
    # path('driver/<int:pk>/', include(router.urls)),
    # path('viewset/', include(router.urls)),
    # path('viewset/<int:pk>/', include(router.urls)),
    # path('client/', GenericAPIView.as_view()),
    # path('client/<int:id>/', GenericAPIView.as_view()),
# ]
