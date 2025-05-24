import pytest
from decimal import Decimal
from accounts.models import CustomUser, AccountBalance
from categories.models import Category
from budget.models import Transaction

@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

@pytest.fixture
def other_user():
    return CustomUser.objects.create_user(
        username='otheruser',
        password='testpass123',
        email='other@example.com'
    )

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client

@pytest.fixture
def category(user):
    return Category.objects.create(
        name='Test Category',
        user=user,
        description='Test Description',
        is_default=False
    )

@pytest.fixture
def balance(user):
    return AccountBalance.objects.create(
        user=user,
        balance=Decimal('1000.00')
    )

@pytest.fixture
def transaction(user, category):
    return Transaction.objects.create(
        user=user,
        category=category,
        amount=Decimal('50.00'),
        type='expense',
        description='Test transaction',
        date='2023-01-01'
    )

