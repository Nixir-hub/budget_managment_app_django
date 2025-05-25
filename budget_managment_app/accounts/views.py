from django.views.generic import FormView, UpdateView, DeleteView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  UserUpdateForm, AccountBalanceForm, CustomUserCreationForm
from .models import CustomUser, AccountBalance
from django.views.generic import TemplateView
from categories.models import Category


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('transaction-list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # saldo = 0
        AccountBalance.objects.get_or_create(user=user, defaults={'balance': 0})

        # saldo - tylko jeśli nie istnieje dlk wystarczających środkówa tego usera (bez względu na wielkość liter)
        if not Category.objects.filter(user=user, name__iexact='Saldo').exists():
            Category.objects.create(
                user=user,
                name='Saldo',
                description='Kategoria systemowa do śledzenia salda',
                is_system=True,
                is_default=False
            )

        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'registration/user_update.html'
    success_url = reverse_lazy('transaction-list')

    def get_object(self):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'registration/user_confirm_delete.html'
    success_url = reverse_lazy('register')

    def get_object(self):
        return self.request.user



class IndexView(TemplateView):
    template_name = 'base.html'

class AccountBalanceUpdateView(LoginRequiredMixin, UpdateView):
    model = AccountBalance
    form_class = AccountBalanceForm
    template_name = 'registration/account_balance_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_object(self):
        # Utwórz obiekt salda, jeśli go nie ma
        obj, _ = AccountBalance.objects.get_or_create(user=self.request.user)
        return obj
