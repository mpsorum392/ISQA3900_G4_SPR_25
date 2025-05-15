from django.urls import path, include
from .views      import signup, NotifyPasswordChangeView

urlpatterns = [
    # allauth’s built-in URLs (login, logout, reset, etc.)
    path('', include('allauth.account.urls')),

    # your signup
    path('signup/', signup, name='signup'),

    # override default password-change to fire your email
    path(
        'password/change/',
        NotifyPasswordChangeView.as_view(),
        name='account_password_change'
    ),
]
