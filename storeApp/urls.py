from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.products, name='products'),
    path('fetchProducts', views.fetchProducts, name='fetchProducts'),
    path('<slug:slug>/', views.details, name='details'),
    path('addReview', csrf_exempt(views.addReview), name='addReview'),
]
