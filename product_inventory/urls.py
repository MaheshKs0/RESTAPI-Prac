from django.urls import path, include
from product_inventory.views import products_view,UserCreationView,OAuth2TokenViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user_creation',UserCreationView,basename='create_user')
router.register('oauth2',OAuth2TokenViewSet,basename='create_token')

urlpatterns = [
    path('productinventory/<str:productid>/',products_view,name='products_view'),
    path('', include(router.urls))

]
