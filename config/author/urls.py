from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AuthorsViewSet

router = DefaultRouter()
router.register(r'author',AuthorsViewSet)

urlpatterns = [
    path('',include(router.urls)),
]