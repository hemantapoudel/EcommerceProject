from .views import ItemViewSet
from rest_framework import routers
from django.urls import path,include
router=routers.DefaultRouter()
router.register('item',ItemViewSet)
urlpatterns = [
    path('', include(router.urls)),   
]