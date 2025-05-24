import pytest
from categories.forms import CategoryForm
from budget.forms import TransactionForm

from accounts.models import AccountBalance
from categories.models import Category

pytestmark = pytest.mark.django_db

class TestCategoryForm:
    def test_valid_category_form(self):
        data = {
            'name': 'Test Category',
            'description': 'Test Description',
            'is_default': False
        }
        form = CategoryForm(data=data)
        assert form.is_valid()

    def test_invalid_category_form(self):
        data = {'name': ''}  # name is required
        form = CategoryForm(data=data)
        assert not form.is_valid()
        assert 'name' in form.errors

class TestTransactionForm:
    def test_valid_transaction_form(self, category):
        data = {
            'category': category.id,
            'amount': '50.00',
            'type': 'expense',
            'description': 'Test transaction',
            'date': '2023-01-01'
        }
        form = TransactionForm(data=data)
        assert form.is_valid()

    def test_invalid_amount(self, category):
        data = {
            'category': category.id,
            'amount': '-50.00',  # negative amount
            'type': 'expense',
            'description': 'Test transaction',
            'date': '2023-01-01'
        }
        form = TransactionForm(data=data)
        assert not form.is_valid()
        assert 'amount' in form.errors

