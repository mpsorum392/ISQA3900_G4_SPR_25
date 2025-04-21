# orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/checkout/', views.checkout, name='checkout'),
    path('<int:order_id>/receipt/',  views.receipt,  name='receipt'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]


