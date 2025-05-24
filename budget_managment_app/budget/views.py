from django.db.models.aggregates import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime
from .forms import TransactionForm
from .models import Transaction


from accounts.models import AccountBalance

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'budget/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        category = self.request.GET.get('category')
        date = self.request.GET.get('date')

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if date:
            queryset = queryset.filter(date=date)

        return queryset


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ← kluczowe!
        return kwargs

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('transaction-list')
    template_name = 'budget/transaction_confirm_delete.html'

    def get_queryset(self):
        return self.request.user.transactions.all()



class BalanceSummaryView(TemplateView):
    template_name = 'budget/summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = datetime.now()
        year, month = now.year, now.month

        transactions = Transaction.objects.filter(user=user, date__year=year, date__month=month)

        income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = income - expense

        context.update({
            'income': income,
            'expense': expense,
            'balance': balance,
            'transactions': transactions,
        })
        return context
