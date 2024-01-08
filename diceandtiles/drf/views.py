from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Comment, Vote, Profile, Fetched_Product, OwnedProduct
from .serializers import UserSerializer,ProductSerializer, CategorySerializer, OwnedProductSerializer, CommentSerializer, VoteSerializer, Fetched_ProductSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication

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

class RegisterViewSet(viewsets.ModelViewSet):
    """
    rejestracja uzytkownikow
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'head']

class CommentViewSet(viewsets.ModelViewSet):
    """
    lista produktów z mikroserwisu fetched przed mergem do main tabeli
    """
    http_method_names = ['head', 'get', 'post']

    serializer_class = CommentSerializer
    authentication_class = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
       
        queryset = Comment.objects.all().order_by('-id')
        product = self.request.data.get('product') 
        owner = self.request.data.get('owner') 
        if product is not None: ##do zwracania komentarzy napisanych pod danym produktem
            queryset = queryset.filter(product=product)
        if owner is not None: ##do zwracania komentarzy napisanych tylko przez danego użytk
            queryset = queryset.filter(owner__username=owner)
        return queryset
    


class VoteViewSet(viewsets.ModelViewSet):
    """
    lista produktów z mikroserwisu fetched przed mergem do main tabeli
    """
    http_method_names = ['post']

    serializer_class = VoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        try:
            product = Product.objects.get(pk=self.request.data.get('product'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'})
        
        existing_vote = Vote.objects.filter(product=product, owner=self.request.user).first()
        if existing_vote:
            # Update the existing vote
            existing_vote.value = self.request.data.get('value', 0)
            existing_vote.save()
        else:
            # Create a new vote
            Vote.objects.create(product=product, owner=self.request.user, value=self.request.data.get('value', 0))

class OwnedProductViewSet(viewsets.ModelViewSet):
    """
    lista posiadanych gier uzytkownika
    """
    http_method_names = ['get','post']

    serializer_class = OwnedProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        try:
            product = Product.objects.get(pk=self.request.data.get('product'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'})
        
        if OwnedProduct.objects.filter(product=product, owner=self.request.user).first():
            return Response({"message": " product is already on your list"})
        else:
            # Create a new vote
            OwnedProduct.objects.create(product=product, owner=self.request.user )
    def get_queryset(self): 
        if self.request.user.is_authenticated:
            return OwnedProduct.objects.filter(owner=self.request.user)
        else:
             return OwnedProduct.objects.none()
 #zwróć obiekty gdzie user w modelu zgadza sie z userem z requesta (wymaga tokenu)
    
   

    
   