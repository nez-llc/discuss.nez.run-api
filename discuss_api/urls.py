from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

from discuss_api.apps.status.views import StatusViewSet


router = routers.DefaultRouter()
router.register('status', StatusViewSet, basename='status')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
