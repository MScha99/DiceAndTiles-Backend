from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Comment, Vote, Profile, Fetched_Product
from .serializers import UserSerializer,ProductSerializer, CategorySerializer, CommentSerializer, VoteSerializer, Fetched_ProductSerializer
from django.contrib.auth.models import User

class ProductPagination(PageNumberPagination):
    page_size = 25  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 2000

class ProductViewSet(viewsets.ModelViewSet):
    """
    lista produktów
    """
    
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer
    ordering = ['id']
    http_method_names = ['head','get']
    lookup_field = "slug"
    pagination_class=ProductPagination


class Fetched_ProductViewSet(viewsets.ModelViewSet):
    """
    lista produktów z mikroserwisu fetched przed mergem do main tabeli
    """
    
    queryset = Fetched_Product.objects.all()
    serializer_class =  Fetched_ProductSerializer
    http_method_names = ['head','get']
    lookup_field = "bggid"

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        response.data['token'] = token.key
        return response
   