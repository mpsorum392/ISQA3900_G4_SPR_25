# DjangoProject/urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    # Home page
    path('', home, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Authentication (django‑allauth + your custom account views)
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),

    # Your app routes
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

    # Orders (namespaced so 'orders:checkout', 'orders:receipt' resolve)
    path('orders/',   include('orders.urls', namespace='orders')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




