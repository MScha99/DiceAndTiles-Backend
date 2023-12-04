from django.contrib import admin
from .models import Product, Comment, Profile, Vote, Fetched_Product



@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']

@admin.register(Fetched_Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','id','slug']

@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product','body','created_on','owner']

@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    
@admin.register(Vote)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['product','value','owner']
