from django.urls import path
from .views import RegisterView, UserUpdateView, UserDeleteView, IndexView, AccountBalanceUpdateView

urlpatterns = [

# Konta użytkowników
path('register/', RegisterView.as_view(), name='register'),
path('account/update/', UserUpdateView.as_view(), name='user-update'),
path('account/delete/', UserDeleteView.as_view(), name='user-delete'),
path('balance/', AccountBalanceUpdateView.as_view(), name='account-balance'),
]