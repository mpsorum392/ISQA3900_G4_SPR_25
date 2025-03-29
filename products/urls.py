from django.urls import path
from .views import products_by_category

urlpatterns = [
    path('category/<str:category_name>/', products_by_category, name='products_by_category'),
]
