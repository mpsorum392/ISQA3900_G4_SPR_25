from django.urls import path
from .views import products_by_category
from . import views

app_name='products'

urlpatterns = [
    path('category/<str:category_name>/', products_by_category, name='products_by_category'),
    path('search/', views.search, name='search'),
]
