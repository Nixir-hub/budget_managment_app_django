import pytest
from django.urls import reverse
from decimal import Decimal
from accounts.models import CustomUser, AccountBalance
from categories.models import Category
from budget.models import Transaction

pytestmark = pytest.mark.django_db

class TestAccountViews:
    def test_register_view(self, client):
        url = reverse('register')
        data = {
            'username': 'testuser2',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'email': 'test2@example.com'
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert CustomUser.objects.filter(username='testuser2').exists()
        assert Category.objects.filter(name='Saldo', user__username='testuser2').exists()


    # def test_user_update_view(self, authenticated_client, user):
    #     url = reverse('user-update')
    #     data = {
    #         'username': user.username,  # pole tylko do odczytu
    #         'email': user.email,        # pole tylko do odczytu
    #         'first_name': 'Zaktualizowane',
    #         'last_name': 'Nazwisko',
    #     }
    #     response = authenticated_client.post(url, data)
    #     user.refresh_from_db()
    #     assert response.status_code == 200
    #     assert user.first_name == 'Zaktualizowane'
    #     assert user.last_name == 'Nazwisko'
    #     # sprawdzamy czy pola tylko do odczytu nie zostały zmienione
    #     assert user.username == 'testuser'
    #     assert user.email == 'test@example.com'


class TestTransactionListView:
    def test_transaction_list_view_requires_login(self, client):
        url = reverse('transaction-list')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_transaction_list_shows_user_transactions(self, authenticated_client, transaction):
        url = reverse('transaction-list')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert len(response.context['transactions']) == 1
        assert response.context['transactions'][0] == transaction

    def test_transaction_list_filters_by_category(self, authenticated_client, user, transaction):
        url = reverse('transaction-list')
        response = authenticated_client.get(url, {'category': transaction.category.name})
        assert response.status_code == 200
        assert len(response.context['transactions']) == 1

    def test_transaction_list_filters_by_date(self, authenticated_client, user, transaction):
        url = reverse('transaction-list')
        response = authenticated_client.get(url, {'date': '2023-01-01'})
        assert response.status_code == 200
        assert len(response.context['transactions']) == 1

class TestCategoryViews:
    def test_category_list_view_requires_login(self, client):
        url = reverse('category-list')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_category_list_view_shows_user_categories(self, authenticated_client, category):
        url = reverse('category-list')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert len(response.context['object_list']) == 1
        assert response.context['object_list'][0] == category

    def test_category_create_view(self, authenticated_client, user):
        url = reverse('category-add')
        data = {
            'name': 'New Category',
            'description': 'Test description',
            'is_default': False
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert Category.objects.filter(name='New Category', user=user).exists()

    def test_category_update_view(self, authenticated_client, category):
        url = reverse('category-edit', kwargs={'pk': category.pk})
        data = {
            'name': 'Updated Category',
            'description': 'Updated description',
            'is_default': False
        }
        response = authenticated_client.post(url, data)
        category.refresh_from_db()
        assert response.status_code == 302
        assert category.name == 'Updated Category'

    def test_cannot_update_system_category(self, authenticated_client, user):
        system_category = Category.objects.create(
            name='Saldo',
            user=user,
            description='System category',
            is_system=True
        )
        url = reverse('category-edit', kwargs={'pk': system_category.pk})
        data = {
            'name': 'Updated Saldo',
            'description': 'Updated description'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        system_category.refresh_from_db()
        assert system_category.name == 'Saldo'

    def test_cannot_delete_system_category(self, authenticated_client, user):
        system_category = Category.objects.create(
            name='Saldo',
            user=user,
            description='System category',
            is_system=True
        )
        url = reverse('category-delete', kwargs={'pk': system_category.pk})
        response = authenticated_client.get(url)  # Najpierw sprawdzamy GET
        assert response.status_code == 404

        # Próba usunięcia przez POST
        response = authenticated_client.post(url)
        assert response.status_code == 404
        assert Category.objects.filter(pk=system_category.pk).exists()
        assert Category.objects.get(pk=system_category.pk).name == 'Saldo'

class TestExpenseChartView:
    def test_expense_chart_requires_login(self, client):
        url = reverse('expense-chart')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_expense_chart_returns_image(self, authenticated_client, transaction):
        url = reverse('expense-chart')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response['Content-Type'] == 'image/png'