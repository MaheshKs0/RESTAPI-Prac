from django.urls import path,include
from rest_framework import routers
from .views import TradeViewSet


router = routers.DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')


urlpatterns = [
    path('',include(router.urls))
]