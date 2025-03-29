#$DjangoProject/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # the home view we just created

urlpatterns = [
    path('', home, name='home'),  # root URL uses our home view
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), # if you have custom signup or profile views

    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]

