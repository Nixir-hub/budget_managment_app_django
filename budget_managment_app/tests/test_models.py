import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from accounts.models import AccountBalance
from categories.models import Category
from budget.models import Transaction
from budget.forms import TransactionForm

pytestmark = pytest.mark.django_db

class TestAccountBalanceModel:
    def test_account_balance_creation(self, balance):
        assert balance.balance == Decimal('1000.00')
        assert str(balance) == f'testuser – 1000.00 zł'

    def test_negative_balance_not_allowed(self, user, category):
        # Tworzymy saldo początkowe
        AccountBalance.objects.create(
            user=user,
            balance=Decimal('100.00')
        )
        
        # Próbujemy utworzyć transakcję przez formularz
        form_data = {
            'category': category.id,
            'amount': '150.00',
            'type': 'expense',
            'date': '2023-01-01',
            'description': 'Test transaction'
        }
        
        form = TransactionForm(data=form_data, user=user)
        assert not form.is_valid()
        assert 'Brak wystarczających środków na koncie.' in str(form.errors)

class TestTransactionModel:
    def test_transaction_creation(self, transaction):
        assert transaction.amount == Decimal('50.00')
        assert transaction.type == 'expense'
        assert transaction.description == 'Test transaction'
        assert str(transaction.date) == '2023-01-01'

    def test_transaction_str(self, user, category):
        transaction = Transaction.objects.create(
            user=user,
            category=category,
            amount=Decimal('50.00'),
            type='expense',
            description='Test transaction',
            date='2023-01-01'
        )
        expected = f'2023-01-01 - {category.name} - 50.00'
        assert str(transaction) == expected