from rest_framework import routers

from django.urls import path, include

router_api = routers.DefaultRouter()

urlpatterns = [
    path('', include(router_api.urls)),
]
