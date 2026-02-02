from rest_framework import viewsets
from .models import Authors
from .serializer import AuthorsSerializers

class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializers