from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import filters, viewsets

from .models import Category
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['=name']
    filter_fields = ['name']
