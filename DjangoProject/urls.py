#$DjangoProject/urls.py
from django.contrib import admin
#added re_path as part of panywhere move
from django.urls import path, include, re_path
from accounts.views import home  # the home view we just created
#added below two for pythonanywhere move
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),  # root URL uses our home view
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), # if you have custom signup or profile views

    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),

    #added below two for pythonanywhere move
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}), #serve media files when deployed
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}), #serve static files when deployed
]

