from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .forms import TransactionForm
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import timedelta, datetime
from django.utils import timezone
import matplotlib
matplotlib.use('Agg')  # Musi być ustawione przed importem pyplot
import matplotlib.pyplot as plt
from django.utils.dateparse import parse_date
import numpy as np
from io import BytesIO
from .models import Transaction
from accounts.models import AccountBalance

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'budget/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        date_str = self.request.GET.get("date")
        if date_str:
            parsed_date = parse_date(date_str)
            if parsed_date:
                queryset = queryset.filter(date=parsed_date)
        return queryset


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # przekazujemy usera do formularza
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        # pełna walidacja formularza
        response = super().form_valid(form)

        return response


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


class ExpenseChartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Pobieranie danych za ostatnie 6 miesięcy
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)

        # Agregacja wydatków po miesiącach
        expenses = (Transaction.objects
                    .filter(user=request.user,
                            type='expense',
                            date__range=[start_date, end_date])
                    .annotate(month=TruncMonth('date'))
                    .values('month', 'category__name')
                    .annotate(total=Sum('amount'))
                    .order_by('month', 'category__name'))

        if not expenses:
            # Jeśli nie ma danych, zwróć pusty wykres
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'Brak danych do wyświetlenia',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes)
            buffer = BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)
            return HttpResponse(buffer.getvalue(), content_type='image/png')

        # Przygotowanie danych do wykresu
        months = sorted(list(set(expense['month'] for expense in expenses)))
        categories = sorted(list(set(expense['category__name'] for expense in expenses)))

        data = np.zeros((len(categories), len(months)))
        for expense in expenses:
            cat_idx = categories.index(expense['category__name'])
            month_idx = months.index(expense['month'])
            data[cat_idx][month_idx] = expense['total']

        # Tworzenie wykresu
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Wykres słupkowy skumulowany
        bottom = np.zeros(len(months))
        for i, category in enumerate(categories):
            ax1.bar([m.strftime('%Y-%m') for m in months],
                    data[i],
                    bottom=bottom,
                    label=category)
            bottom += data[i]

        ax1.set_title('Wydatki miesięczne według kategorii')
        ax1.set_xlabel('Miesiąc')
        ax1.set_ylabel('Kwota (PLN)')
        ax1.legend(title='Kategorie', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

        # Wykres kołowy dla sumy wydatków w kategoriach
        total_by_category = data.sum(axis=1)
        if total_by_category.sum() > 0:  # Sprawdzamy czy są jakieś wydatki
            ax2.pie(total_by_category,
                    labels=categories,
                    autopct='%1.1f%%',
                    textprops={'fontsize': 8})
            ax2.set_title('Udział kategorii w wydatkach')
        else:
            ax2.text(0.5, 0.5, 'Brak wydatków',
                     horizontalalignment='center',
                     verticalalignment='center',
                     transform=ax2.transAxes)

        # Dostosowanie układu
        plt.tight_layout()

        # Zapisanie wykresu do bufora
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close(fig)  # Ważne: zamknij wykres aby zwolnić pamięć
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type='image/png')
