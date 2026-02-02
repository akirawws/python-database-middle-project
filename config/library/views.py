from rest_framework import viewsets
from .models import Library
from .serializer import LibrarySerializers

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializers