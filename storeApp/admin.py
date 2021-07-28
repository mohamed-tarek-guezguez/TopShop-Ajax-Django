from django.contrib import admin
from .models import Product, Review

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['Title', 'Price', 'CreatedAt']
    ordering = ['-CreatedAt']
    search_fields = ('Title', 'Price', 'CreatedAt')

admin.site.register(Product, ProductAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'date_posted', 'comment', 'post_connected']
    ordering = ['-date_posted']
    search_fields = ('user', 'rating', 'date_posted', 'comment')

admin.site.register(Review, ReviewAdmin)