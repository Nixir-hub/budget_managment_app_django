from django.urls import path, include
from .views import TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView, \
    BalanceSummaryView

urlpatterns = [
    # Transakcje
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', TransactionCreateView.as_view(), name='transaction-add'),
    path('transactions/<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('summary/', BalanceSummaryView.as_view(), name='balance-summary'),
]