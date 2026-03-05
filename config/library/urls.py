from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    AuthorViewSet,
    GenreViewSet,
    ClientViewSet,
    ReviewViewSet,
    BookLoanViewSet,
    PublisherViewSet,
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')    
router.register(r'genres', GenreViewSet, basename='genre')     
router.register(r'clients', ClientViewSet, basename='client')      
router.register(r'reviews', ReviewViewSet, basename='review')     
router.register(r'bookloans', BookLoanViewSet, basename='bookloan') 
router.register(r'publishers', PublisherViewSet, basename='publisher') 

urlpatterns = [
    path('', include(router.urls)),
]